"""

    Performance Test: Dataplane Throughput Test: nat Mode
    pytest -m "dataplane_throughput_test and nat"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.performance, pytest.mark.dataplane_throughput_test,
              pytest.mark.nat]

setup_params_general = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa2_personal": [
            {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["2G"], "security_key": "something"},
            {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["5G"], "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.suite("performance")
@allure.feature("BRIDGE MODE Dataplane Throughput Test")
@allure.feature("NAT MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestDataplaneThroughputNAT(object):
    """Dataplane THroughput nat Mode
       pytest -m "dataplane_throughput_test and nat"
    """
    
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3913", name="WIFI-3913")
    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_tcp_upd_wpa2_personal_nat_2g_band(self, get_vif_state, lf_tools,
                             lf_test, station_names_twog, create_lanforge_chamberview_dut,
                             get_configuration):
        """Dataplane THroughput nat Mode
           pytest -m "dataplane_throughput_test and nat and wpa2_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_DPT_DPT_WPA2_2G_NAT",
                                       vlan_id=vlan, dut_name=dut_name)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Dataplane Throughput Test - TCP-UDP 2.4G")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-3914", name="WIFI-3914")
    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_tcp_upd_wpa2_personal_nat_5g_band(self, get_vif_state, lf_tools,
                             lf_test, station_names_fiveg, create_lanforge_chamberview_dut, get_configuration):
        """Dataplane THroughput nat Mode
           pytest -m "dataplane_throughput_test and nat and wpa2_personal and fiveg"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "NAT"
        band = "fiveg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security,
                                         passkey=security_key, mode=mode, band=band,
                                         station_name=station_names_fiveg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fiveg, mode=mode,
                                       instance_name="TIP_DPT_DPT_WPA2_5G_NAT",
                                       vlan_id=vlan, dut_name=dut_name)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            lf_tools.attach_report_graphs(report_name=report_name, pdf_name="Dataplane Throughput Test - TCP-UDP 5G")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fiveg)
            assert station
        else:
            assert False
