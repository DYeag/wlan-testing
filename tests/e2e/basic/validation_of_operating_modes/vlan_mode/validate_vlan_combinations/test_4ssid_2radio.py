import os
import pytest
import allure

pytestmark = [pytest.mark.vlan_combination_test, pytest.mark.four_ssid_two_radio,
              pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "wpa2_personal": [{"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "vlan": 9},
                          {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "vlan": 10},
                          {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "vlan": 11},
                          {"ssid_name": "ssid_wpa2_2g", "appliedRadios": ["is2dot4GHz"], "vlan": 12},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 13},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 14},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 15},
                          {"ssid_name": "ssid_wpa2_5g", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 16}]},

    "rf": {},
    "radius": False
}


@pytest.mark.four_ssid_two_radio
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
class TestValidFourSsidTwoRadio(object):

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_wpa2_ssid_2g(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                          update_report, test_cases):
        '''
            pytest -m "vlan_combination_test and four_ssid_two_radio and wpa2_personal and twog
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
        lf_test.Client_disconnect(station_names_twog)
        lf_test.Client_Connect(ssid=ssid_name, security=security,
                               passkey=security_key, mode=mode, band=band,
                               station_name=station_names_twog, vlan_id=vlan)

        sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                        port_data[1] + "/" + port_data[2] + "." + str(vlan) + "?fields=ip")[
            "interface"]["ip"]

        sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                   port_data[1] + "/" + station_names_twog[0] + "?fields=ip")["interface"]["ip"]
        lf_test.Client_disconnect(station_names_twog)

        for m, n in zip(sta_ip[0:2], sta_vlan_ip[0:2]):
            if m != n:
                assert False

        print("All stations got ip as per vlan")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_wpa2_ssid_2g(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                          update_report, test_cases):
        '''
            pytest -m "vlan_combination_test and four_ssid_two_radio and wpa2_personal and twog
        '''

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = profile_data["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        lf_test.Client_Connect(ssid=ssid_name, security=security,
                               passkey=security_key, mode=mode, band=band,
                               station_name=station_names_twog, vlan_id=vlan)

        sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                        port_data[1] + "/" + port_data[2] + "." + str(vlan) + "?fields=ip")[
            "interface"]["ip"]

        sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                   port_data[1] + "/" + station_names_twog[0] + "?fields=ip")["interface"]["ip"]
        lf_test.Client_disconnect(station_names_twog)

        for m, n in zip(sta_ip[0:2], sta_vlan_ip[0:2]):
            if m != n:
                assert False

        print("All stations got ip as per vlan")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_wpa2_ssid_2g(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                          update_report, test_cases):
        '''
            pytest -m "vlan_combination_test and four_ssid_two_radio and wpa2_personal and twog
        '''

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][2]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = profile_data["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        lf_test.Client_Connect(ssid=ssid_name, security=security,
                               passkey=security_key, mode=mode, band=band,
                               station_name=station_names_twog, vlan_id=vlan)

        sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                        port_data[1] + "/" + port_data[2] + "." + str(vlan) + "?fields=ip")[
            "interface"]["ip"]

        sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                   port_data[1] + "/" + station_names_twog[0] + "?fields=ip")["interface"]["ip"]
        lf_test.Client_disconnect(station_names_twog)

        for m, n in zip(sta_ip[0:2], sta_vlan_ip[0:2]):
            if m != n:
                assert False

        print("All stations got ip as per vlan")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.twog
    def test_wpa2_ssid_2g(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                          update_report, test_cases):
        '''
            pytest -m "vlan_combination_test and four_ssid_two_radio and wpa2_personal and twog
        '''

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][3]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "twog"
        vlan = profile_data["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        lf_test.Client_Connect(ssid=ssid_name, security=security,
                               passkey=security_key, mode=mode, band=band,
                               station_name=station_names_twog, vlan_id=vlan)

        sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                        port_data[1] + "/" + port_data[2] + "." + str(vlan) + "?fields=ip")[
            "interface"]["ip"]

        sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                   port_data[1] + "/" + station_names_twog[0] + "?fields=ip")["interface"]["ip"]
        lf_test.Client_disconnect(station_names_twog)

        for m, n in zip(sta_ip[0:2], sta_vlan_ip[0:2]):
            if m != n:
                assert False

        print("All stations got ip as per vlan")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_wpa2_ssid_5g(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                          update_report, test_cases):
        '''
            pytest -m "vlan_combination_test and four_ssid_two_radio and wpa2_personal and fiveg
        '''

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][4]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = profile_data["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        lf_test.Client_Connect(ssid=ssid_name, security=security,
                               passkey=security_key, mode=mode, band=band,
                               station_name=station_names_fiveg, vlan_id=vlan)

        sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                        port_data[1] + "/" + port_data[2] + "." + str(vlan) + "?fields=ip")[
            "interface"]["ip"]

        sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                   port_data[1] + "/" + station_names_fiveg[0] + "?fields=ip")["interface"]["ip"]

        lf_test.Client_disconnect(station_names_fiveg)

        for m, n in zip(sta_ip[0:2], sta_vlan_ip[0:2]):
            if m != n:
                assert False

        print("All stations got ip as per vlan")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_wpa2_ssid_5g(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                          update_report, test_cases):
        '''
            pytest -m "vlan_combination_test and four_ssid_two_radio and wpa2_personal and fiveg
        '''

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][5]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = profile_data["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        lf_test.Client_Connect(ssid=ssid_name, security=security,
                               passkey=security_key, mode=mode, band=band,
                               station_name=station_names_fiveg, vlan_id=vlan)

        sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                        port_data[1] + "/" + port_data[2] + "." + str(vlan) + "?fields=ip")[
            "interface"]["ip"]

        sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                   port_data[1] + "/" + station_names_fiveg[0] + "?fields=ip")["interface"]["ip"]

        lf_test.Client_disconnect(station_names_fiveg)

        for m, n in zip(sta_ip[0:2], sta_vlan_ip[0:2]):
            if m != n:
                assert False

        print("All stations got ip as per vlan")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_wpa2_ssid_5g(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                          update_report, test_cases):
        '''
            pytest -m "vlan_combination_test and four_ssid_two_radio and wpa2_personal and fiveg
        '''

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][6]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = profile_data["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        lf_test.Client_Connect(ssid=ssid_name, security=security,
                               passkey=security_key, mode=mode, band=band,
                               station_name=station_names_fiveg, vlan_id=vlan)

        sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                        port_data[1] + "/" + port_data[2] + "." + str(vlan) + "?fields=ip")[
            "interface"]["ip"]

        sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                   port_data[1] + "/" + station_names_fiveg[0] + "?fields=ip")["interface"]["ip"]

        lf_test.Client_disconnect(station_names_fiveg)

        for m, n in zip(sta_ip[0:2], sta_vlan_ip[0:2]):
            if m != n:
                assert False

        print("All stations got ip as per vlan")
        assert True

    @pytest.mark.wpa2_personal
    @pytest.mark.fiveg
    def test_wpa2_ssid_5g(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                          update_report, test_cases):
        '''
            pytest -m "vlan_combination_test and four_ssid_two_radio and wpa2_personal and fiveg
        '''

        profile_data = setup_params_general["ssid_modes"]["wpa2_personal"][7]
        ssid_name = profile_data["ssid_name"]
        security_key = profile_data["security_key"]
        security = "wpa2"
        mode = "VLAN"
        band = "fiveg"
        vlan = profile_data["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        lf_test.Client_Connect(ssid=ssid_name, security=security,
                               passkey=security_key, mode=mode, band=band,
                               station_name=station_names_fiveg, vlan_id=vlan)

        sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                        port_data[1] + "/" + port_data[2] + "." + str(vlan) + "?fields=ip")[
            "interface"]["ip"]

        sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                   port_data[1] + "/" + station_names_fiveg[0] + "?fields=ip")["interface"]["ip"]

        lf_test.Client_disconnect(station_names_fiveg)

        for m, n in zip(sta_ip[0:2], sta_vlan_ip[0:2]):
            if m != n:
                assert False

        print("All stations got ip as per vlan")
        assert True

