"""

    Client Connectivity Enterprise TTLS
    pytest -m "client_connectivity and bridge and enterprise and ttls"

"""
import allure
import pytest

pytestmark = [pytest.mark.client_connectivity, pytest.mark.bridge, pytest.mark.enterprise, pytest.mark.ttls,
              pytest.mark.ucentral, pytest.mark.sanity]  # , pytest.mark.usefixtures("setup_test_run")]

setup_params_enterprise = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa_enterprise": [
            {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_wpa_eap_5g", "appliedRadios": ["5G"]}],
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["5G"]}],
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["5G"]}]},

    "rf": {},
    "radius": True
}


@allure.suite(suite_name="sanity")
@allure.sub_suite(sub_suite_name="Bridge Mode EAP Client Connectivity : Suite-A")
@pytest.mark.suiteA
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeEnterpriseTTLSSuiteA(object):
    """ SuiteA Enterprise Test Cases
        pytest -m "client_connectivity and bridge and enterprise and ttls and suiteA"
    """

    @pytest.mark.wpa_enterprise
    @pytest.mark.twog
    def test_wpa_enterprise_2g(self, get_vif_state, get_ap_logs,
                               station_names_twog, setup_profiles, get_lanforge_data, lf_test, update_report,
                               test_cases, radius_info, exit_on_fail):
        """ wpa enterprise 2g
            pytest -m "client_connectivity and bridge and enterprise and ttls and wpa_enterprise and twog"
        """
        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, vlan_id=vlan)

        assert passes

    @pytest.mark.wpa_enterprise
    @pytest.mark.fiveg
    def test_wpa_enterprise_5g(self, station_names_fiveg, get_ap_logs,
                               setup_profiles, get_lanforge_data, lf_test, update_report,
                               test_cases, radius_info, exit_on_fail):
        """ wpa enterprise 5g
            pytest -m "client_connectivity and bridge and enterprise and ttls and wpa_enterprise and fiveg"
        """
        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, vlan_id=vlan)
        assert passes

    @pytest.mark.uc_sanity
    @pytest.mark.sanity_light
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    def test_wpa2_enterprise_2g(self, get_vif_state, get_ap_logs,
                                station_names_twog, setup_profiles, get_lanforge_data, lf_test, update_report,
                                test_cases, radius_info, exit_on_fail):
        """ wpa enterprise 2g
            pytest -m "client_connectivity and bridge and enterprise and ttls and wpa2_enterprise and twog"
        """
        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, vlan_id=vlan)
        assert passes

    @pytest.mark.uc_sanity
    @pytest.mark.sanity_light
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    def test_wpa2_enterprise_5g(self, get_vif_state, get_ap_logs,
                                station_names_fiveg, setup_profiles, get_lanforge_data, lf_test, update_report,
                                test_cases, radius_info, exit_on_fail):
        """ wpa enterprise 2g
            pytest -m "client_connectivity and bridge and enterprise and ttls and wpa2_enterprise and fiveg"
        """
        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, vlan_id=vlan)

        assert passes
    
    @pytest.mark.uc_sanity
    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    def test_wpa3_enterprise_2g(self, get_vif_state, get_ap_logs,
                                station_names_twog, setup_profiles, get_lanforge_data, lf_test, update_report,
                                test_cases, radius_info, exit_on_fail):
        """ wpa enterprise 2g
            pytest -m "client_connectivity and bridge and enterprise and ttls and wpa3_enterprise and twog"
        """
        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band, ieee80211w=2, key_mgmt="WPA-EAP-SHA256",
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, vlan_id=vlan)

        assert passes
    
    @pytest.mark.uc_sanity
    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    def test_wpa3_enterprise_5g(self, get_vif_state, get_ap_logs,
                                station_names_fiveg, setup_profiles, get_lanforge_data, lf_test, update_report,
                                test_cases, radius_info, exit_on_fail):
        """ wpa enterprise 2g
            pytest -m "client_connectivity and bridge and enterprise and ttls and wpa3_enterprise and fiveg"
        """
        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band, ieee80211w=2, key_mgmt="WPA-EAP-SHA256",
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, vlan_id=vlan)

        assert passes


setup_params_enterprise_two = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa_wpa2_enterprise_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_wpa_wpa2_eap_5g", "appliedRadios": ["5G"]}],
        "wpa3_enterprise_mixed": [
            {"ssid_name": "ssid_wpa3_mixed_eap_2g", "appliedRadios": ["2G"]},
            {"ssid_name": "ssid_wpa3_mixed_eap_5g", "appliedRadios": ["5G"]}]
    },
    "rf": {},
    "radius": True
}


@allure.suite(suite_name="sanity")
@allure.sub_suite(sub_suite_name="Bridge Mode EAP Client Connectivity : Suite-B")
@pytest.mark.suiteB
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestBridgeModeEnterpriseTTLSSuiteTwo(object):
    """ SuiteA Enterprise Test Cases
        pytest -m "client_connectivity and bridge and enterprise and ttls and suiteB"
    """

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.twog
    def test_wpa_wpa2_enterprise_2g(self, get_vif_state, get_ap_logs,
                                    station_names_twog, setup_profiles, get_lanforge_data, lf_test, update_report,
                                    test_cases, radius_info, exit_on_fail):
        """ wpa enterprise 2g
            pytest -m "client_connectivity and bridge and enterprise and ttls and wpa_wpa2_enterprise_mixed and twog"
        """
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa_wpa2_enterprise_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, vlan_id=vlan)

        assert passes

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.fiveg
    def test_wpa_wpa2_enterprise_5g(self, get_vif_state, get_ap_logs,
                                    station_names_fiveg, setup_profiles, get_lanforge_data, lf_test,
                                    update_report, test_cases, radius_info, exit_on_fail):
        """ wpa enterprise 2g
            pytest -m "client_connectivity and bridge and enterprise and ttls and wpa_wpa2_enterprise_mixed and fiveg"
        """
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa_wpa2_enterprise_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, vlan_id=vlan)

        assert passes

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.twog
    def test_wpa3_enterprise_mixed_2g(self, get_vif_state, get_ap_logs,
                                      station_names_twog, setup_profiles, get_lanforge_data, lf_test,
                                      update_report, test_cases, radius_info, exit_on_fail):
        """ wpa enterprise 2g
            pytest -m "client_connectivity and bridge and enterprise and ttls and wpa3_enterprise_mixed and twog"
        """
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa3_enterprise_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "twog"
        vlan = 1
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, vlan_id=vlan)

        assert passes

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.fiveg
    def test_wpa3_enterprise_mixed_5g(self, get_vif_state, get_ap_logs,
                                      station_names_fiveg, setup_profiles, get_lanforge_data, lf_test,
                                      update_report, exit_on_fail,
                                      test_cases, radius_info):
        """ wpa enterprise 2g
            pytest -m "client_connectivity and bridge and enterprise and ttls and wpa3_enterprise_mixed and fiveg"
        """
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa3_enterprise_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"
        mode = "BRIDGE"
        band = "fiveg"
        vlan = 1
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, vlan_id=vlan)

        assert passes
