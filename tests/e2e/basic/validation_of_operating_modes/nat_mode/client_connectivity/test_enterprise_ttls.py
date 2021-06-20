import allure
import pytest

mode = "NAT"

pytestmark = [pytest.mark.client_connectivity, pytest.mark.usefixtures("setup_test_run"), pytest.mark.nat,
              pytest.mark.enterprise, pytest.mark.ttls,
              pytest.mark.sanity]

setup_params_enterprise = {
    "mode": mode,
    "ssid_modes": {
        "wpa_enterprise": [
            {"ssid_name": "ssid_wpa_eap_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa2_enterprise": [
            {"ssid_name": "ssid_wpa2_eap_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa2_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa3_enterprise": [
            {"ssid_name": "ssid_wpa3_eap_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa3_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}]},

    "rf": {},
    "radius": True
}


@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestNATModeEnterpriseTTLSSuiteOne(object):

    @pytest.mark.wpa_enterprise
    @pytest.mark.twog
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wpa_enterprise_2g(self, get_vif_state,station_names_twog, setup_profiles, get_lanforge_data, lf_test, update_report,
                               test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]

        band = "twog"
        vlan = 1
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        identity = radius_info['user']
        ieee80211w = 1
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                     mode=mode, band=band, ieee80211w=ieee80211w,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, vlan_id=vlan)

        if passes:
            update_report.update_testrail(case_id=test_cases["2g_wpa_eap_ttls_nat"],
                                          status_id=1,
                                          msg='2G WPA Enterprise Client Connectivity Passed successfully - NAT mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["2g_wpa_eap_ttls_nat"],
                                          status_id=5,
                                          msg='2G WPA Enterprise Client Connectivity Failed - NAT mode' + str(
                                              passes))
            if exit_on_fail:
                pytest.exit("Test Case Failed")
        assert passes

    @pytest.mark.wpa_enterprise
    @pytest.mark.fiveg
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wpa_enterprise_5g(self, get_vif_state,station_names_fiveg, setup_profiles, get_lanforge_data, lf_test, update_report,
                               test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]

        band = "fiveg"
        vlan = 1
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        pairwise = "CCMP"
        group = "CCMP"
        ieee80211w =1
        identity = radius_info['user']
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security, extra_securities=extra_secu,
                                     mode=mode, band=band, group=group, pairwise=pairwise, ieee80211w=ieee80211w,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, vlan_id=vlan)

        if passes:
            update_report.update_testrail(case_id=test_cases["5g_wpa_eap_ttls_nat"],
                                          status_id=1,
                                          msg='5G WPA Enterprise Client Connectivity Passed successfully - NAT mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["5g_wpa_eap_ttls_nat"],
                                          status_id=5,
                                          msg='5G WPA Enterprise Client Connectivity Failed - NAT mode' + str(
                                              passes))
            if exit_on_fail:
                pytest.exit("Test Case Failed")
        assert passes

    @pytest.mark.sanity_light
    @pytest.mark.wpa2_enterprise
    @pytest.mark.twog
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wpa2_enterprise_2g(self, get_vif_state,station_names_twog, setup_profiles, get_lanforge_data, lf_test, update_report,
                                test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"

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

        if passes:
            update_report.update_testrail(case_id=test_cases["2g_wpa2_eap_ttls_nat"],
                                          status_id=1,
                                          msg='2G WPA2 Enterprise Client Connectivity Passed successfully - NAT mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["2g_wpa2_eap_ttls_nat"],
                                          status_id=5,
                                          msg='2G WPA2 Enterprise Client Connectivity Failed - NAT mode' + str(
                                              passes))
            if exit_on_fail:
                pytest.exit("Test Case Failed")
        assert passes

    @pytest.mark.sanity_light
    @pytest.mark.wpa2_enterprise
    @pytest.mark.fiveg
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wpa2_enterprise_5g(self, get_vif_state, station_names_fiveg, setup_profiles, get_lanforge_data, lf_test, update_report,
                                test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa2_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa2"

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

        if passes:
            update_report.update_testrail(case_id=test_cases["5g_wpa2_eap_ttls_nat"],
                                          status_id=1,
                                          msg='5G WPA2 Enterprise Client Connectivity Passed successfully - NAT mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["5g_wpa2_eap_ttls_nat"],
                                          status_id=5,
                                          msg='5G WPA2 Enterprise Client Connectivity Failed - NAT mode' + str(
                                              passes))
            if exit_on_fail:
                pytest.exit("Test Case Failed")
        assert passes

    @pytest.mark.wpa3_enterprise
    @pytest.mark.twog
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wpa3_enterprise_2g(self, get_vif_state,station_names_twog, setup_profiles, get_lanforge_data, lf_test, update_report,
                                test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"

        band = "twog"
        vlan = 1
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        key_mgmt = "WPA-EAP-SHA256"
        identity = radius_info['user']
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band, key_mgmt=key_mgmt,
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_twog, vlan_id=vlan)

        if passes:
            update_report.update_testrail(case_id=test_cases["2g_wpa3_eap_ttls_nat"],
                                          status_id=1,
                                          msg='2G WPA3 Enterprise Client Connectivity Passed successfully - NAT mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["2g_wpa3_eap_ttls_nat"],
                                          status_id=5,
                                          msg='2G WPA3 Enterprise Client Connectivity Failed - NAT mode' + str(
                                              passes))
            if exit_on_fail:
                pytest.exit("Test Case Failed")
        assert passes

    @pytest.mark.wpa3_enterprise
    @pytest.mark.fiveg
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wpa3_enterprise_5g(self, get_vif_state,station_names_fiveg, setup_profiles, get_lanforge_data, lf_test, update_report,
                                test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise["ssid_modes"]["wpa3_enterprise"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"

        band = "fiveg"
        vlan = 1
        ttls_passwd = radius_info["password"]
        eap = "TTLS"
        key_mgmt = "WPA-EAP-SHA256"
        identity = radius_info['user']
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        passes = lf_test.EAP_Connect(ssid=ssid_name, security=security,
                                     mode=mode, band=band, key_mgmt = "WPA-EAP-SHA256",
                                     eap=eap, ttls_passwd=ttls_passwd, identity=identity,
                                     station_name=station_names_fiveg, vlan_id=vlan)

        if passes:
            update_report.update_testrail(case_id=test_cases["5g_wpa3_eap_ttls_nat"],
                                          status_id=1,
                                          msg='5G WPA3 Enterprise Client Connectivity Passed successfully - NAT mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["5g_wpa3_eap_ttls_nat"],
                                          status_id=5,
                                          msg='5G WPA3 Enterprise Client Connectivity Failed - NAT mode' + str(
                                              passes))
            if exit_on_fail:
                pytest.exit("Test Case Failed")
        assert passes


setup_params_enterprise_two = {
    "mode": mode,
    "ssid_modes": {
        "wpa_wpa2_enterprise_mixed": [
            {"ssid_name": "ssid_wpa_wpa2_eap_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa_wpa2_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa3_enterprise_mixed": [
            {"ssid_name": "ssid_wpa3_mixed_eap_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa3_mixed_eap_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}]
    },
    "rf": {},
    "radius": True
}


@pytest.mark.enterprise
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_enterprise_two],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestNATModeEnterpriseTTLSSuiteTwo(object):

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.twog
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wpa_wpa2_enterprise_mixed_2g(self, get_vif_state,station_names_twog, setup_profiles, get_lanforge_data, lf_test, update_report,
                                    test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa_wpa2_enterprise_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]

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

        if passes:
            update_report.update_testrail(case_id=test_cases["2g_wpa2_mixed_eap_ttls_wpa2_nat"],
                                          status_id=1,
                                          msg='2G WPA2 Mixed Enterprise Client Connectivity Passed successfully - NAT mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["2g_wpa2_mixed_eap_ttls_wpa2_nat"],
                                          status_id=5,
                                          msg='2G WPA2 Mixed Enterprise Client Connectivity Failed - NAT mode' + str(
                                              passes))
            if exit_on_fail:
                pytest.exit("Test Case Failed")
        assert passes

    @pytest.mark.wpa_wpa2_enterprise_mixed
    @pytest.mark.fiveg
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wpa_wpa2_enterprise_mixed_5g(self, get_vif_state,station_names_fiveg, setup_profiles, get_lanforge_data, lf_test,
                                    update_report, test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa_wpa2_enterprise_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa"
        extra_secu = ["wpa2"]

        band = "fievg"
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

        if passes:
            update_report.update_testrail(case_id=test_cases["5g_wpa2_mixed_eap_ttls_wpa2_nat"],
                                          status_id=1,
                                          msg='5G WPA2 Mixed Enterprise Client Connectivity Passed successfully - NAT mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["5g_wpa2_mixed_eap_ttls_wpa2_nat"],
                                          status_id=5,
                                          msg='5G WPA2 Mixed Client Connectivity Failed - NAT mode' + str(
                                              passes))
            if exit_on_fail:
                pytest.exit("Test Case Failed")
        assert passes

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.twog
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wpa3_enterprise_mixed_2g(self, get_vif_state,station_names_twog, setup_profiles, get_lanforge_data, lf_test,
                                      update_report, test_cases, radius_info, exit_on_fail):
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa3_enterprise_mixed"][0]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"

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

        if passes:
            update_report.update_testrail(case_id=test_cases["2g_wpa3_mixed_eap_ttls_wpa3_nat"],
                                          status_id=1,
                                          msg='2G WPA3 Mixed Enterprise Client Connectivity Passed successfully - NAT mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["2g_wpa3_mixed_eap_ttls_wpa3_nat"],
                                          status_id=5,
                                          msg='2G WPA3 Mixed Enterprise Client Connectivity Failed - NAT mode' + str(
                                              passes))
            if exit_on_fail:
                pytest.exit("Test Case Failed")
        assert passes

    @pytest.mark.wpa3_enterprise_mixed
    @pytest.mark.fiveg
    def test_wpa3_enterprise_mixed_5g(self, get_vif_state, station_names_fiveg, setup_profiles, get_lanforge_data, lf_test,
                                      update_report, exit_on_fail, test_cases, radius_info):
        profile_data = setup_params_enterprise_two["ssid_modes"]["wpa3_enterprise_mixed"][1]
        ssid_name = profile_data["ssid_name"]
        security = "wpa3"

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

        if passes:
            update_report.update_testrail(case_id=test_cases["5g_wpa3_mixed_eap_ttls_wpa3_nat"],
                                          status_id=1,
                                          msg='5G WPA3 Mixed Enterprise Client Connectivity Passed successfully - NAT mode' + str(
                                              passes))
        else:
            update_report.update_testrail(case_id=test_cases["5g_wpa3_mixed_eap_ttls_wpa3_nat"],
                                          status_id=5,
                                          msg='5G WPA3 Mixed Enterprise Client Connectivity Failed - NAT mode' + str(
                                              passes))
            if exit_on_fail:
                pytest.exit("Test Case Failed")
        assert passes
