import os
import allure
import pytest

pytestmark = [pytest.mark.vlan_combination_test,
              pytest.mark.vlan_ping_test,pytest.mark.usefixtures("setup_test_run")]


setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2p_2g", "appliedRadios": ["is2dot4GHz"], "security_key": "something", "vlan": 790},
            {"ssid_name": "ssid_wpa2p_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"],
             "security_key": "something", "vlan": 80}]},
    "rf": {},
    "radius": False
}


@pytest.mark.vlan_ping_test
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    "setup_profiles",
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.parametrize(
    "create_vlan",
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles", "create_vlan")
class TestValidVlan(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_wpa2_ssid_2g(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                          get_vlan_list, update_report, test_cases):
        '''
            pytest -m "vlan_combination_test and vlan_ping_test and wpa2_personal and twog
        '''

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = profile_data["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        vlan_list = get_vlan_list
        print(vlan_list)
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan, cleanup=False)
        if result:
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2] + "." + str(vlan) + "?fields=ip")[
                "interface"]["ip"]

            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0] + "?fields=ip")["interface"]["ip"]

            sta_ip = sta_ip.split(".")
            sta_vlan_ip = sta_vlan_ip.split(".")
            print(sta_ip[:2], sta_vlan_ip[:2])
            for m, n in zip(sta_ip[0:2], sta_vlan_ip[0:2]):
                if m != n:
                    assert False
            vlan_list = [int(i) for i in vlan_list]
            if int(vlan) in vlan_list:
                print("All stations got ip as per vlan")
                assert True
            else:
                assert False
            ping_obj = lf_test.gen_test(station_names_twog)
            print("generic started")
            print("helloo..", ping_obj.created_endp)
            gen_results = lf_tools.json_get("generic/list?fields=name,last+results")
            print(gen_results)
            if gen_results['endpoints'] is not None:
                for name in gen_results['endpoints']:
                    for k, v in name.items():
                        if v['name'] in ping_obj.created_endp and not v['name'].endswith('1'):
                            if v['last results'] != "" and "Unreachable" not in v['last results']:
                                print("ping successful")
                                assert True

                            else:
                                print("ping unsuccessful")
                                assert False
            try:
                lf_test.Client_disconnect(station_names_twog)
            except:
                pass

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_wpa2_ssid_5g(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                          get_vlan_list, update_report, test_cases):
        '''
            pytest -m "vlan_combination_test and vlan_ping_test and wpa2_personal and fiveg
        '''

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = profile_data["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        vlan_list = get_vlan_list
        print(vlan_list)
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan, cleanup=False)
        if result:
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2] + "." + str(vlan) + "?fields=ip")[
                "interface"]["ip"]

            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0] + "?fields=ip")["interface"]["ip"]

            sta_ip = sta_ip.split(".")
            sta_vlan_ip = sta_vlan_ip.split(".")
            print(sta_ip[:2], sta_vlan_ip[:2])
            for m, n in zip(sta_ip[0:2], sta_vlan_ip[0:2]):
                if m != n:
                    assert False
            vlan_list = [int(i) for i in vlan_list]
            if int(vlan) in vlan_list:
                print("All stations got ip as per vlan")
                assert True
            else:
                assert False
            ping_obj = lf_test.gen_test(station_names_fiveg)
            print("generic started")
            print("helloo..", ping_obj.created_endp)
            gen_results = lf_tools.json_get("generic/list?fields=name,last+results")
            print(gen_results)
            if gen_results['endpoints'] is not None:
                for name in gen_results['endpoints']:
                    for k, v in name.items():
                        if v['name'] in ping_obj.created_endp and not v['name'].endswith('1'):
                            if v['last results'] != "" and "Unreachable" not in v['last results']:
                                print("ping successful")
                                assert True

                            else:
                                print("ping unsuccessful")
                                assert False
            try:
                lf_test.Client_disconnect(station_names_fiveg)
            except:
                pass
