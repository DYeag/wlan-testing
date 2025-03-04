"""

    Base Library for Ucentral

"""
import json
import ssl
import sys
import time
from urllib.parse import urlparse
import pytest
import allure
import requests
from pathlib import Path

from requests.adapters import HTTPAdapter
import logging


# logging.basicConfig(level=logging.DEBUG)
# from http.client import HTTPConnection
#
# HTTPConnection.debuglevel = 1
# requests.logging.getLogger()


class ConfigureController:

    def __init__(self, controller_data):
        self.username = controller_data["username"]
        self.password = controller_data["password"]
        self.host = urlparse(controller_data["url"])
        print(self.host)
        self.access_token = ""
        # self.session = requests.Session()
        self.login_resp = self.login()
        self.gw_host, self.fms_host = self.get_gw_endpoint()
        if self.gw_host == "" or self.fms_host == "":
            time.sleep(60)
            self.gw_host, self.fms_host = self.get_gw_endpoint()
            if self.gw_host == "" or self.fms_host == "":
                self.logout()
                print(self.gw_host, self.fms_host)
                pytest.exit("All Endpoints not available in Controller Service")
                sys.exit()

    def build_uri_sec(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.host.hostname, self.host.port, path)
        print(new_uri)
        return new_uri

    def build_url_fms(self, path):
        new_uri = 'https://%s:%d/api/v1/%s' % (self.fms_host.hostname, self.fms_host.port, path)
        print(new_uri)
        return new_uri

    def build_uri(self, path):

        new_uri = 'https://%s:%d/api/v1/%s' % (self.gw_host.hostname, self.gw_host.port, path)
        print(new_uri)
        return new_uri

    def request(self, service, command, method, params, payload):
        if service == "sec":
            uri = self.build_uri_sec(command)
        elif service == "gw":
            uri = self.build_uri(command)
        elif service == "fms":
            uri = self.build_url_fms(command)
        else:
            raise NameError("Invalid service code for request.")

        print(uri)
        params = params
        if method == "GET":
            resp = requests.get(uri, headers=self.make_headers(), params=params, verify=False, timeout=100)
        elif method == "POST":
            resp = requests.post(uri, data=payload, verify=False, timeout=100)
        elif method == "PUT":
            resp = requests.put(uri, data=payload, verify=False, timeout=100)
        elif method == "DELETE":
            resp = requests.delete(uri, headers=self.make_headers(), params=params, verify=False, timeout=100)

        self.check_response(method, resp, self.make_headers(), payload, uri)
        print(resp)
        return resp

    def login(self):
        uri = self.build_uri_sec("oauth2")
        # self.session.mount(uri, HTTPAdapter(max_retries=15))
        payload = json.dumps({"userId": self.username, "password": self.password})
        resp = requests.post(uri, data=payload, verify=False, timeout=100)
        self.check_response("POST", resp, "", payload, uri)
        token = resp.json()
        self.access_token = token["access_token"]
        print(token)

        # self.session.headers.update({'Authorization': self.access_token})
        return resp

    def get_gw_endpoint(self):
        uri = self.build_uri_sec("systemEndpoints")
        print(uri)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        print(resp)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        services = resp.json()
        print(services)
        gw_host = ""
        fms_host = ""
        for service in services['endpoints']:
            if service['type'] == "ucentralgw":
                gw_host = urlparse(service["uri"])
            if service['type'] == "ucentralfms":
                fms_host = urlparse(service["uri"])
        return gw_host, fms_host

    def logout(self):
        uri = self.build_uri_sec('oauth2/%s' % self.access_token)
        resp = requests.delete(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("DELETE", resp, self.make_headers(), "", uri)
        print('Logged out:', resp.status_code)
        return resp

    def make_headers(self):
        headers = {'Authorization': 'Bearer %s' % self.access_token,
                   "Connection": "keep-alive",
                   "Keep-Alive": "timeout=10, max=1000"
                   }
        return headers

    def check_response(self, cmd, response, headers, data_str, url):
        if response.status_code >= 400:
            if response.status_code >= 400:
                print("check-response: ERROR, url: ", url)
            else:
                print("check-response: url: ", url)
            print("Command: ", cmd)
            print("response-status: ", response.status_code)
            print("response-headers: ", response.headers)
            print("response-content: ", response.content)
            print("headers: ", headers)
            print("data-str: ", data_str)

        if response.status_code >= 400:
            # if True:
            raise NameError("Invalid response code.")
        return True


class Controller(ConfigureController):

    def __init__(self, controller_data=None):
        super().__init__(controller_data)

    def get_devices(self):
        uri = self.build_uri("devices/")
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        devices = resp.json()
        # resp.close()()
        return devices

    def get_device_by_serial_number(self, serial_number=None):
        uri = self.build_uri("device/" + serial_number)
        resp = requests.get(uri, headers=self.make_headers(), verify=False, timeout=100)
        self.check_response("GET", resp, self.make_headers(), "", uri)
        device = resp.json()
        # resp.close()()
        return device

    def get_device_uuid(self, serial_number):
        device_info = self.get_device_by_serial_number(serial_number=serial_number)
        return device_info["UUID"]


class FMSUtils:

    def __init__(self, sdk_client=None, controller_data=None):
        if sdk_client is None:
            self.sdk_client = Controller(controller_data=controller_data)
        self.sdk_client = sdk_client

    def upgrade_firmware(self, serial="", url=""):
        response = self.sdk_client.request(service="gw", command="device/" + serial + "upgrade/",
                                           method="POST", params="revisionSet=true",
                                           payload="{ \"serialNumber\" : " + serial + " , \"uri\" : " + url + " }")
        print(response)
        pass

    def ap_model_lookup(self, model=""):
        devices = self.get_device_set()
        model_name = ""
        for device in devices['deviceTypes']:
            if str(device).__contains__(model):
                model_name = device
        return model_name

    def get_revisions(self):
        response = self.sdk_client.request(service="fms", command="firmwares/", method="GET", params="revisionSet=true",
                                           payload="")
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def get_latest_fw(self, model=""):

        device_type = self.ap_model_lookup(model=model)

        response = self.sdk_client.request(service="fms", command="firmwares/", method="GET",
                                           params="latestOnly=true&deviceType=" + device_type,
                                           payload="")
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def get_device_set(self):
        response = self.sdk_client.request(service="fms", command="firmwares/", method="GET", params="deviceSet=true",
                                           payload="")
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def get_firmwares(self, limit="", deviceType="", latestonly=""):

        params = "limit=" + limit + "&deviceType=" + deviceType + "&latestonly=" + latestonly

        response = self.sdk_client.request(service="fms", command="firmwares/", method="GET", params=params, payload="")
        print(response)
        if response.status_code == 200:
            data = response.json()
            print(data)

        # resp = requests.get(uri, headers=self.sdk_client.make_headers(), verify=False, timeout=100)
        # self.sdk_client.check_response("GET", resp, self.sdk_client.make_headers(), "", uri)
        # devices = resp.json()
        # # resp.close()()
        return "devices"


class UProfileUtility:

    def __init__(self, sdk_client=None, controller_data=None):
        if sdk_client is None:
            self.sdk_client = Controller(controller_data=controller_data)
        self.sdk_client = sdk_client
        self.base_profile_config = {
            "uuid": 1,
            "radios": [],
            "interfaces": [{
                "name": "WAN",
                "role": "upstream",
                "services": ["ssh", "lldp", "dhcp-snooping"],
                "ethernet": [
                    {
                        "select-ports": [
                            "WAN*"
                        ]
                    }
                ],
                "ipv4": {
                    "addressing": "dynamic"
                }
            },
                {
                    "name": "LAN",
                    "role": "downstream",
                    "services": ["ssh", "lldp", "dhcp-snooping"],
                    "ethernet": [
                        {
                            "select-ports": [
                                "LAN*"
                            ]
                        }
                    ],
                    "ipv4": {
                        "addressing": "static",
                        "subnet": "192.168.1.1/16",
                        "dhcp": {
                            "lease-first": 10,
                            "lease-count": 10000,
                            "lease-time": "6h"
                        }
                    },
                }],
            "metrics": {
                "statistics": {
                    "interval": 60,
                    "types": ["ssids", "lldp", "clients"]
                },
                "health": {
                    "interval": 120
                },
                "wifi-frames": {
                    "filters": ["probe",
                                "auth",
                                "assoc",
                                "disassoc",
                                "deauth",
                                "local-deauth",
                                "inactive-deauth",
                                "key-mismatch",
                                "beacon-report",
                                "radar-detected"]
                },
                "dhcp-snooping": {
                    "filters": ["ack", "discover", "offer", "request", "solicit", "reply", "renew"]
                }
            },
            "services": {
                "lldp": {
                    "describe": "TIP OpenWiFi",
                    "location": "QA"
                },
                "ssh": {
                    "port": 22
                }
            }
        }
        self.vlan_section = {
            "name": "WAN100",
            "role": "upstream",
            "vlan": {
                "id": 100
            },
            "ethernet": [
                {
                    "select-ports": [
                        "WAN*"
                    ]
                }
            ],
            "ipv4": {
                "addressing": "dynamic"
            }
        }
        self.mode = None

    def encryption_lookup(self, encryption="psk"):
        encryption_mapping = {
            "none": "open",
            "psk": "wpa",
            "psk2": "wpa2",
            "sae": "wpa3",
            "psk-mixed": "wpa|wpa2",
            "sae-mixed": "wpa3",
            "wpa": 'wap',
            "wpa2": "eap",
            "wpa3": "eap",
            "wpa-mixed": "eap",
            "wpa3-mixed": "sae"
        }
        if encryption in encryption_mapping.keys():
            return encryption_mapping[encryption]
        else:
            return False

    def get_ssid_info(self):
        ssid_info = []
        for interfaces in self.base_profile_config["interfaces"]:
            if "ssids" in interfaces.keys():
                for ssid_data in interfaces["ssids"]:
                    for band in ssid_data["wifi-bands"]:
                        temp = [ssid_data["name"]]
                        if ssid_data["encryption"]["proto"] == "none" or "radius" in ssid_data.keys():
                            temp.append(self.encryption_lookup(encryption=ssid_data["encryption"]["proto"]))
                            temp.append('[BLANK]')
                        else:
                            temp.append(self.encryption_lookup(encryption=ssid_data["encryption"]["proto"]))
                            temp.append(ssid_data["encryption"]["key"])
                        temp.append(band)
                        ssid_info.append(temp)
        return ssid_info

    def set_radio_config(self, radio_config=None):
        self.base_profile_config["radios"].append({
            "band": "2G",
            "country": "US",
            # "channel-mode": "HE",
            "channel-width": 20,
            # "channel": 11
        })
        self.base_profile_config["radios"].append({
            "band": "5G",
            "country": "US",
            # "channel-mode": "HE",
            "channel-width": 80,
            # "channel": "auto"
        })

        self.vlan_section["ssids"] = []
        self.vlan_ids = []

    def set_mode(self, mode):
        self.mode = mode
        if mode == "NAT":
            self.base_profile_config['interfaces'][1]['ssids'] = []
        elif mode == "BRIDGE":
            self.base_profile_config['interfaces'][0]['ssids'] = []
        elif mode == "VLAN":
            del self.base_profile_config['interfaces'][1]
            self.base_profile_config['interfaces'][0]['ssids'] = []
            self.base_profile_config['interfaces'] = []
            wan_section_vlan = {
                "name": "WAN",
                "role": "upstream",
                "services": ["lldp", "ssh", "dhcp-snooping"],
                "ethernet": [
                    {
                        "select-ports": [
                            "WAN*"
                        ]
                    }
                ],
                "ipv4": {
                    "addressing": "dynamic"
                }
            }
            self.base_profile_config['interfaces'].append(wan_section_vlan)
        else:
            print("Invalid Mode")
            return 0

    def add_ssid(self, ssid_data, radius=False, radius_auth_data={}, radius_accounting_data={}):
        print("ssid data : ", ssid_data)
        ssid_info = {'name': ssid_data["ssid_name"], "bss-mode": "ap", "wifi-bands": [], "services": ["wifi-frames"]}
        for options in ssid_data:
            if options == "multi-psk":
                ssid_info[options] = ssid_data[options]
                print("hi", ssid_info)
            if options == "rate-limit":
                ssid_info[options] = ssid_data[options]
        for i in ssid_data["appliedRadios"]:
            ssid_info["wifi-bands"].append(i)
        ssid_info['encryption'] = {}
        ssid_info['encryption']['proto'] = ssid_data["security"]
        try:
            ssid_info['encryption']['key'] = ssid_data["security_key"]
        except Exception as e:
            pass
        ssid_info['encryption']['ieee80211w'] = "optional"
        if radius:
            ssid_info["radius"] = {}
            ssid_info["radius"]["authentication"] = {
                "host": radius_auth_data["ip"],
                "port": radius_auth_data["port"],
                "secret": radius_auth_data["secret"]
            }
            ssid_info["radius"]["accounting"] = {
                "host": radius_accounting_data["ip"],
                "port": radius_accounting_data["port"],
                "secret": radius_accounting_data["secret"]
            }
        if self.mode == "NAT":
            self.base_profile_config['interfaces'][1]['ssids'].append(ssid_info)
        elif self.mode == "BRIDGE":
            self.base_profile_config['interfaces'][0]['ssids'].append(ssid_info)
        elif self.mode == "VLAN":
            vid = ssid_data["vlan"]
            self.vlan_section = {
                "name": "WAN100",
                "role": "upstream",
                "services": ["lldp", "dhcp-snooping"],
                "vlan": {
                    "id": 100
                },
                "ethernet": [
                    {
                        "select-ports": [
                            "WAN*"
                        ]
                    }
                ],
                "ipv4": {
                    "addressing": "dynamic"
                }
            }
            vlan_section = self.vlan_section
            if vid in self.vlan_ids:
                print("sss", self.vlan_ids)
                for i in self.base_profile_config['interfaces']:
                    if i["name"] == "WANv%s" % (vid):
                        i["ssids"].append(ssid_info)
            else:
                print(self.vlan_ids)
                self.vlan_ids.append(vid)
                vlan_section['name'] = "WANv%s" % (vid)
                vlan_section['vlan']['id'] = int(vid)
                vlan_section["ssids"] = []
                vlan_section["ssids"].append(ssid_info)
                self.base_profile_config['interfaces'].append(vlan_section)
                print(vlan_section)
                vsection = 0
        else:
            print("invalid mode")
            pytest.exit("invalid Operating Mode")

    def push_config(self, serial_number):
        payload = {"configuration": self.base_profile_config, "serialNumber": serial_number, "UUID": 0}

        uri = self.sdk_client.build_uri("device/" + serial_number + "/configure")
        basic_cfg_str = json.dumps(payload)
        print(self.base_profile_config)
        allure.attach(name="ucentral_config: ",
                      body=str(self.base_profile_config).replace("'", '"'),
                      attachment_type=allure.attachment_type.JSON)
        print(self.base_profile_config)
        resp = requests.post(uri, data=basic_cfg_str, headers=self.sdk_client.make_headers(),
                             verify=False, timeout=100)
        self.sdk_client.check_response("POST", resp, self.sdk_client.make_headers(), basic_cfg_str, uri)
        print(resp.url)
        resp.close()
        print(resp)


if __name__ == '__main__':
    controller = {
        'url': 'https://sec-ucentral-qa01.cicd.lab.wlan.tip.build:16001',  # API base url for the controller
        'username': "tip@ucentral.com",
        'password': 'openwifi',
    }
    obj = Controller(controller_data=controller)
    fms = FMSUtils(sdk_client=obj)
    # fms.get_device_set()
    # model = fms.get_latest_fw(model="eap102")
    # print(model)
    # profile = UProfileUtility(sdk_client=obj)
    # profile.set_mode(mode="BRIDGE")
    # profile.set_radio_config()
    # ssid = {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G", "5G"], "security": "psk", "security_key": "something",
    #         "vlan": 100}
    # profile.add_ssid(ssid_data=ssid, radius=False)
    # profile.push_config(serial_number="903cb39d6918")
    # print(profile.get_ssid_info())
    # # print(obj.get_devices())
    obj.logout()
