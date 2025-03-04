"""

    Performance Test: Throughput vs Various Pkt Size Test: VLAN MODE
    pytest -m "throughput_vs_pkt and vlan"

"""
import os
import pytest
import allure

pytestmark = [pytest.mark.throughput_vs_pkt, pytest.mark.vlan, pytest.mark.wpa,
              pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["5G"],
                 "security_key": "something"}]},

    "rf": {},
    "radius": False
}


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_general],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa
class TestThroughputVsPktVlanWpa2G(object):
    """Throughput vs Various Pkt Size Test vlan mode
       pytest -m "throughput_vs_pkt and vlan"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2548", name="WIFI-2548")
    @pytest.mark.wpa_personal
    @pytest.mark.twog
    @pytest.mark.pkt60
    def test_client_wpa_personal_pkt_60_2g(self, get_vif_state,
                                           lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                           get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and wpa_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa_personal"
        mode = "VLAN"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 60'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA_VLAN_2G_60",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2548", name="WIFI-2548")
    @pytest.mark.wpa_personal
    @pytest.mark.twog
    @pytest.mark.pkt142
    def test_client_wpa_personal_pkt_142_2g(self, get_vif_state,
                                            lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                            get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and wpa_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa_personal"
        mode = "VLAN"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 142'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA_VLAN_2G_142",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2548", name="WIFI-2548")
    @pytest.mark.wpa_personal
    @pytest.mark.twog
    @pytest.mark.pkt256
    def test_client_wpa_personal_pkt_256_2g(self, get_vif_state,
                                            lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                            get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and wpa_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa_personal"
        mode = "VLAN"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 256'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA_VLAN_2G_256",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2548", name="WIFI-2548")
    @pytest.mark.wpa_personal
    @pytest.mark.twog
    @pytest.mark.pkt512
    def test_client_wpa_personal_pkt_512_2g(self, get_vif_state,
                                            lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                            get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and wpa_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa_personal"
        mode = "VLAN"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 512'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA_VLAN_2G_512",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2548", name="WIFI-2548")
    @pytest.mark.wpa_personal
    @pytest.mark.twog
    @pytest.mark.pkt1024
    def test_client_wpa_personal_pkt_1024_2g(self, get_vif_state,
                                             lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                             get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and wpa_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa_personal"
        mode = "VLAN"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 1024'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA_VLAN_2G_1024",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2548", name="WIFI-2548")
    @pytest.mark.wpa_personal
    @pytest.mark.twog
    @pytest.mark.pktMTU
    def test_client_wpa_personal_pkt_MTU_2g(self, get_vif_state,
                                            lf_test, station_names_twog, create_lanforge_chamberview_dut,
                                            get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and wpa_personal and twog"
        """
        profile_data = setup_params_general["ssid_modes"]["wpa_personal"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa_personal"
        mode = "VLAN"
        band = "twog"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: MTU'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_twog, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_twog, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA_VLAN_2G_MTU",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_twog)
            assert station
        else:
            assert False


setup_params_5g = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa": [{"ssid_name": "ssid_wpa_2g", "appliedRadios": ["2G"], "security_key": "something"},
                {"ssid_name": "ssid_wpa_5g", "appliedRadios": ["5G"],
                 "security_key": "something"}]},
    "rf": {},
    "radius": False
}


@allure.feature("VLAN MODE CLIENT CONNECTIVITY")
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_5g],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
@pytest.mark.wpa
class TestThroughputVsPktVlan5G(object):
    """Throughput vs Various Pkt Size Test vlan mode
       pytest -m "throughput_vs_pkt and vlan"
    """
    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2548", name="WIFI-2548")
    @pytest.mark.wpa_personal
    @pytest.mark.fivg
    @pytest.mark.pkt60
    def test_client_wpa_personal_pkt_60_5g(self, get_vif_state,
                                           lf_test, station_names_fivg, create_lanforge_chamberview_dut,
                                           get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and wpa_personal and fivg"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa_personal"
        mode = "VLAN"
        band = "fivg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 60'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_fivg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fivg, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA_VLAN_5G_60",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fivg)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2548", name="WIFI-2548")
    @pytest.mark.wpa_personal
    @pytest.mark.fivg
    @pytest.mark.pkt142
    def test_client_wpa_personal_pkt_142_5g(self, get_vif_state,
                                            lf_test, station_names_fivg, create_lanforge_chamberview_dut,
                                            get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and wpa_personal and fivg"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa_personal"
        mode = "VLAN"
        band = "fivg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 142'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_fivg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fivg, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA_VLAN_5G_142",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fivg)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2548", name="WIFI-2548")
    @pytest.mark.wpa_personal
    @pytest.mark.fivg
    @pytest.mark.pkt256
    def test_client_wpa_personal_pkt_256_5g(self, get_vif_state,
                                            lf_test, station_names_fivg, create_lanforge_chamberview_dut,
                                            get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and wpa_personal and fivg"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa_personal"
        mode = "VLAN"
        band = "fivg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 256'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_fivg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fivg, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA_VLAN_5G",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fivg)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2548", name="WIFI-2548")
    @pytest.mark.wpa_personal
    @pytest.mark.fivg
    @pytest.mark.pkt512
    def test_client_wpa_personal_pkt_512_5g(self, get_vif_state,
                                            lf_test, station_names_fivg, create_lanforge_chamberview_dut,
                                            get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and wpa_personal and fivg"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa_personal"
        mode = "VLAN"
        band = "fivg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 512'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_fivg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fivg, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA_VLAN_5G_512",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fivg)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2548", name="WIFI-2548")
    @pytest.mark.wpa_personal
    @pytest.mark.fivg
    @pytest.mark.pkt1024
    def test_client_wpa_personal_pkt_1024_5g(self, get_vif_state,
                                             lf_test, station_names_fivg, create_lanforge_chamberview_dut,
                                             get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and wpa_personal and fivg"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa_personal"
        mode = "VLAN"
        band = "fivg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: 1024'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_fivg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fivg, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA_VLAN_5G_1024",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fivg)
            assert station
        else:
            assert False

    @allure.testcase(url="https://telecominfraproject.atlassian.net/browse/WIFI-2548", name="WIFI-2548")
    @pytest.mark.wpa_personal
    @pytest.mark.fivg
    @pytest.mark.pktMTU
    def test_client_wpa_personal_pkt_MTU_5g(self, get_vif_state,
                                            lf_test, station_names_fivg, create_lanforge_chamberview_dut,
                                            get_configuration):
        """Throughput Vs Pkt Sizes VLAN MODE
           pytest -m "throughput_vs_pkt and vlan and wpa_personal and fivg"
        """
        profile_data = setup_params_5g["ssid_modes"]["wpa_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa_personal"
        mode = "VLAN"
        band = "fivg"
        vlan = 1
        dut_name = create_lanforge_chamberview_dut
        raw_lines = [['pkts: MTU'],
                     ['directions: DUT Transmit;DUT Receive'],
                     ['traffic_types: UDP;TCP'], ["show_3s: 1"],
                     ["show_ll_graphs: 1"], ["show_log: 1"]]
        if ssid_name not in get_vif_state:
            allure.attach(name="retest,vif state ssid not available:", body=str(get_vif_state))
            pytest.xfail("SSID NOT AVAILABLE IN VIF STATE")
        station = lf_test.Client_Connect(ssid=ssid_name, security=security, passkey=security_key,
                                         mode=mode, band=band,
                                         station_name=station_names_fivg, vlan_id=vlan)

        if station:
            dp_obj = lf_test.dataplane(station_name=station_names_fivg, mode=mode,
                                       instance_name="TIP_PERF_THRU_PKT_WPA_VLAN_5G_MTU",
                                       vlan_id=vlan, dut_name=dut_name, raw_lines=raw_lines)
            report_name = dp_obj.report_name[0]['LAST']["response"].split(":::")[1].split("/")[-1]
            entries = os.listdir("../reports/" + report_name + '/')
            pdf = False
            for i in entries:
                if ".pdf" in i:
                    pdf = i
            if pdf:
                allure.attach.file(source="../reports/" + report_name + "/" + pdf,
                                   name=get_configuration["access_point"][0]["model"] + "_dataplane")
            print("Test Completed... Cleaning up Stations")
            lf_test.Client_disconnect(station_name=station_names_fivg)
            assert station
        else:
            assert False
