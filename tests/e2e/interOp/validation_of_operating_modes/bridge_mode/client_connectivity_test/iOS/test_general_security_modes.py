from logging import exception
import io
import unittest
import warnings
from perfecto.test import TestResultFactory
import pytest
import sys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException

import sys
import allure

if 'perfecto_libs' not in sys.path:
    sys.path.append(f'../libs/perfecto_libs')

from iOS_lib import closeApp, openApp, get_WifiIPAddress_iOS, ForgetWifiConnection, ping_deftapps_iOS, \
    Toggle_AirplaneMode_iOS, set_APconnMobileDevice_iOS, verify_APconnMobileDevice_iOS, Toggle_WifiMode_iOS, tearDown,\
    verifyUploadDownloadSpeediOS, get_ip_address_ios, wifi_connect, wifi_disconnect_and_forget

pytestmark = [pytest.mark.sanity, pytest.mark.interop, pytest.mark.ios, pytest.mark.interop_ios,
              pytest.mark.client_connectivity, pytest.mark.interop_uc_sanity, pytest.mark.bridge]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["2G"]},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["5G"]}],
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["5G"],
                 "security_key": "something"}],
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.suite(suite_name="interop sanity")
@allure.sub_suite(sub_suite_name="Bridge Mode Client Connect : Suite-A")
@pytest.mark.InteropsuiteA
@allure.feature("BRIDGE MODE CLIENT CONNECT")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteOne(object):
    """ Client Connect SuiteA
        pytest -m "client_connect and bridge and InteropsuiteA"
    """

    @pytest.mark.fiveg
    @pytest.mark.wpa2_personal
    def test_ClientConnect_5g_WPA2_Personal(self, request, get_vif_state, get_APToMobileDevice_data,
                                          setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
            assert verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @pytest.mark.twog
    @pytest.mark.wpa2_personal
    def test_ClientConnect_2g_WPA2_Personal(self, request, get_vif_state, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
            assert verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @pytest.mark.fiveg
    @pytest.mark.wpa
    def test_ClientConnect_5g_WPA(self, request, get_vif_state, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
            assert verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @pytest.mark.twog
    @pytest.mark.wpa
    def test_ClientConnect_2g_WPA(self, request, get_vif_state, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["wpa"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
            assert verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @pytest.mark.fiveg
    @pytest.mark.open
    def test_ClientConnect_5g_Open(self, request, get_vif_state, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        #Set Wifi/AP Mode
        ip, is_internet =  get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
            assert verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False

    @pytest.mark.twog
    @pytest.mark.open
    def test_ClientConnect_2g_Open(self, request, get_vif_state, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = "[BLANK]"
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)
        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        if is_internet:
            if ip:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + "with Internet, couldn't get IP address")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))

            wifi_connect(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
            assert verifyUploadDownloadSpeediOS(request, setup_perfectoMobile_iOS, connData)
            wifi_disconnect_and_forget(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)
        else:
            allure.attach(name="Connection Status: ", body=str("No Internet access"))
            assert False





setup_params_general_two = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa3_personal": [
            {"ssid_name": "ssid_wpa3_p_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_5g", "appliedRadios": ["5G"],
             "security_key": "something"}],
        "wpa3_personal_mixed": [
            {"ssid_name": "ssid_wpa3_p_m_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa3_p_m_5g", "appliedRadios": ["5G"],
             "security_key": "something"}],
        "wpa_wpa2_personal_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_p_m_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa_wpa2_p_m_5g", "appliedRadios": ["5G"],
             "security_key": "something"}]
    },
    "rf": {},
    "radius": False
}


@allure.suite(suite_name="interop sanity")
@allure.sub_suite(sub_suite_name="Bridge Mode Client Connect : Suite-B")
@pytest.mark.InteropsuiteB
@allure.feature("BRIDGE MODE CLIENT CONNECT")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeConnectSuiteTwo(object):
    """ Client Connect SuiteA
        pytest -m "client_connect and bridge and InteropsuiteB"
    """

    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal
    def test_ClientConnect_5g_wpa3_personal(self, request, get_vif_state, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    @pytest.mark.twog
    @pytest.mark.wpa3_personal
    def test_ClientConnect_2g_wpa3_personal(self, request, get_vif_state, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    @pytest.mark.fiveg
    @pytest.mark.wpa3_personal_mixed
    def test_ClientConnect_5g_wpa3_personal_mixed(self, request, get_vif_state, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal_mixed"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    @pytest.mark.twog
    @pytest.mark.wpa3_personal_mixed
    def test_ClientConnect_2g_wpa3_personal_mixed(self, request, get_vif_state, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa3_personal_mixed"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

    @pytest.mark.fiveg
    @pytest.mark.wpa_wpa2_personal_mixed
    def test_ClientConnect_5g_wpa_wpa2_personal_mixed(self, request, get_vif_state, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa_wpa2_personal_mixed"][1]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]

        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        #Set Wifi/AP Mode
        ip, is_internet =  get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False


    @pytest.mark.twog
    @pytest.mark.wpa_wpa2_personal_mixed
    def test_ClientConnect_2g_wpa_wpa2_personal_mixed(self, request, get_vif_state, get_APToMobileDevice_data, setup_perfectoMobile_iOS):

        profile_data = setup_params_general_two["ssid_modes"]["wpa_wpa2_personal_mixed"][0]
        ssidName = profile_data["ssid_name"]
        ssidPassword = profile_data["security_key"]
        # ssidPassword = "[BLANK]"
        print ("SSID_NAME: " + ssidName)
        print ("SSID_PASS: " + ssidPassword)
        get_vif_state.append(ssidName)

        if ssidName not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")

        report = setup_perfectoMobile_iOS[1]
        driver = setup_perfectoMobile_iOS[0]
        connData = get_APToMobileDevice_data

        # Set Wifi/AP Mode
        ip, is_internet = get_ip_address_ios(request, ssidName, ssidPassword, setup_perfectoMobile_iOS, connData)

        if ip:
            if is_internet:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "with internet")
            else:
                text_body = ("connected to " + ssidName + " (" + ip + ") " + "without internet")
            print(text_body)
            allure.attach(name="Connection Status: ", body=str(text_body))
            assert True
        else:
            allure.attach(name="Connection Status: ", body=str("Device is Unable to connect"))
            assert False

