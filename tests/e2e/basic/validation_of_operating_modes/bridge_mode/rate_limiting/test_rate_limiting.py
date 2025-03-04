"""
Rate LImiting Bridge Mode Scenario
"""

import allure
import pytest

pytestmark = [pytest.mark.rate_limiting, pytest.mark.bridge, pytest.mark.general, pytest.mark.ucentral,
              pytest.mark.regression]

setup_params_general = {
    "mode": "BRIDGE",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g_br",
             "appliedRadios": ["2G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 100,
                 "egress-rate": 100
             }
             },
            {"ssid_name": "ssid_wpa2_5g_br",
             "appliedRadios": ["5G"],
             "security_key": "something",
             "rate-limit": {
                 "ingress-rate": 100,
                 "egress-rate": 100
             }
             }]},
    "rf": {},
    "radius": False
}


@allure.feature("Bridge MODE Rate Limiting")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestRateLimitingBridge(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.up
    @pytest.mark.batch_size_125
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_batch_size_125_2g(self, lf_test, get_vif_state, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and up and batch_size_125"
        """
        # run wifi capacity test here
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="1,2,5",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.dw
    @pytest.mark.batch_size_125
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_dw_batch_size_125_2g(self, lf_test, get_vif_state, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and dw and batch_size_125"
        """
        # run wifi capacity test here
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2,5",
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.up_dw
    @pytest.mark.batch_size_125
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_dw_batch_size_125_2g(self, lf_test, get_vif_state, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and up_dw and batch_size_125"
        """
        # run wifi capacity test here
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2,5",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up
    @pytest.mark.batch_size_125
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_batch_size_125_5g(self, lf_test, get_vif_state, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and up and batch_size_125"
        """
        # run wifi capacity test here
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="5G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="1,2,5",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dw
    @pytest.mark.batch_size_125
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_dw_batch_size_125_5g(self, lf_test, get_vif_state, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and dw and batch_size_125"
        """
        # run wifi capacity test here
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="5G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2,5",
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up_dw
    @pytest.mark.batch_size_125
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_dw_batch_size_125_5g(self, lf_test, get_vif_state, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and up_dw and batch_size_125"
        """
        # run wifi capacity test here
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="5G", num_stations=5, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1,2,5",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.up
    @pytest.mark.batch_size_1
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_batch_size_1_2g(self, lf_test, get_vif_state, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and up and batch_size_1"
        """
        # run wifi capacity test here
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="1",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.dw
    @pytest.mark.batch_size_1
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_dw_batch_size_1_2g(self, lf_test, get_vif_state, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and dw and batch_size_1"
        """
        # run wifi capacity test here
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    @pytest.mark.up_dw
    @pytest.mark.batch_size_1
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_dw_batch_size_1_2g(self, lf_test, get_vif_state, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and twog and up_dw and batch_size_1"
        """
        # run wifi capacity test here
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="2G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up
    @pytest.mark.batch_size_1
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_batch_size_1_5g(self, lf_test, get_vif_state, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and up and batch_size_1"
        """
        # run wifi capacity test here
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="0Gbps", batch_size="1",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.dw
    @pytest.mark.batch_size_1
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_dw_batch_size_1_5g(self, lf_test, get_vif_state, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and dw and batch_size_1"
        """
        # run wifi capacity test here
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="0Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    @pytest.mark.up_dw
    @pytest.mark.batch_size_1
    @allure.story('Rate Limiting Open SSID 2.4 GHZ Band')
    def test_wpa2_personal_ssid_up_dw_batch_size_1_5g(self, lf_test, get_vif_state, lf_tools):
        """
            Test Rate Limiting Scenario
            pytest -m "rate_limiting and bridge and wpa2_personal and fiveg and up_dw and batch_size_1"
        """
        # run wifi capacity test here
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        mode = "BRIDGE"
        vlan = 1
        allure.attach(name="ssid-rates", body=str(profile_data["rate-limit"]))
        get_vif_state.append(ssid_name)
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        lf_tools.add_stations(band="5G", num_stations=1, dut=lf_tools.dut_name, ssid_name=ssid_name)
        lf_tools.Chamber_View()
        wct_obj = lf_test.wifi_capacity(instance_name="test_client_wpa2_BRIDGE_tcp_dl", mode=mode, vlan_id=vlan,
                                        download_rate="1Gbps", batch_size="1",
                                        upload_rate="1Gbps", protocol="UDP-IPv4", duration="60000")

        report_name = wct_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]

        lf_tools.attach_report_graphs(report_name=report_name)
        print("Test Completed... Cleaning up Stations")
        assert True
