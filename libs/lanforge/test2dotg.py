import os
import allure
import pytest

pytestmark = [pytest.mark.validate_vlan_combination,
              pytest.mark.usefixtures("setup_test_run")]

setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["is2dot4GHz"], "vlan": 2},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"], "vlan": 2}]},
    "rf": {},
    "radius": False
}


@pytest.mark.validate_vlan_combination
@pytest.mark.wifi5
@pytest.mark.wifi6
@pytest.mark.parametrize(
    'setup_profiles',
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

    @pytest.mark.open
    @pytest.mark.twog
    @pytest.mark.valid_vlan_open_2g
    def test_open_ssid_2g(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                          update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = profile_data["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    @pytest.mark.open
    @pytest.mark.fiveg
    def test_open_ssid_5g(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                          update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = profile_data["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False


setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g", "appliedRadios": ["is2dot4GHz"], "vlan": 4096},
                 {"ssid_name": "ssid_open_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"], "vlan": 4096}]},
    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
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
class TestInValidVlan(object):
    @pytest.mark.open
    @pytest.mark.twog
    def test_open_ssid_2g(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                          update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][0]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    @pytest.mark.open
    @pytest.mark.fiveg
    def test_open_ssid_5g(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                          update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][1]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False


setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g_1", "appliedRadios": ["is2dot4GHz"], "vlan": 3},
                 {"ssid_name": "ssid_open_2g_2", "appliedRadios": ["is2dot4GHz"], "vlan": 4},
                 {"ssid_name": "ssid_open_5g_1", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 5},
                 {"ssid_name": "ssid_open_5g_2", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 6},
                 {"ssid_name": "ssid_open_5gU_1", "appliedRadios": ["is5GHzU", "is5GHz"], "vlan": 7},
                 {"ssid_name": "ssid_open_5gU_2", "appliedRadios": ["is5GHzU", "is5GHz"], "vlan": 8}]},

    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
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
class Test2dotg5gUniqueValidVLAN(object):
    @pytest.mark.open
    def test_open_ssid_2g_1(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][0]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_2g_2(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][1]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_1(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][2]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][2]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_2(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][3]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][3]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5gU_1(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][4]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][4]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5gU_2(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][5]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][5]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False


setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g_3", "appliedRadios": ["is2dot4GHz"], "vlan": 9},
                 {"ssid_name": "ssid_open_2g_4", "appliedRadios": ["is2dot4GHz"], "vlan": 10},
                 {"ssid_name": "ssid_open_2g_5", "appliedRadios": ["is2dot4GHz"], "vlan": 11},
                 {"ssid_name": "ssid_open_2g_6", "appliedRadios": ["is2dot4GHz"], "vlan": 12},
                 {"ssid_name": "ssid_open_5g_3", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 13},
                 {"ssid_name": "ssid_open_5g_4", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 14},
                 {"ssid_name": "ssid_open_5g_5", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 15},
                 {"ssid_name": "ssid_open_5g_6", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 16}]},

    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
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
class Test2dotg5g4ssidUniqueValidVLAN(object):
    @pytest.mark.open
    def test_open_ssid_2g_3(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][0]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_2g_4(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][1]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_2g_5(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][2]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][2]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_2g_6(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][3]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][3]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_3(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][4]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][4]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_4(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][5]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][5]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_5(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][6]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_6(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][7]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][7]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False


setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_5g_7", "appliedRadios": ["is5GHzU", "is5GHz"], "vlan": 17},
                 {"ssid_name": "ssid_open_5g_8", "appliedRadios": ["is5GHzU", "is5GHz"], "vlan": 18},
                 {"ssid_name": "ssid_open_5g_9", "appliedRadios": ["is5GHzU", "is5GHz"], "vlan": 19},
                 {"ssid_name": "ssid_open_5g_10", "appliedRadios": ["is5GHzU", "is5GHz"], "vlan": 20}]},

    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
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
class Test5g4ssidUniqueValidVLAN(object):
    def test_open_ssid_5g_7(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][0]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_8(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][1]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_9(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][2]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][2]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_10(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][3]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][3]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False


setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_2g_7", "appliedRadios": ["is2dot4GHz"], "vlan": 21},
                 {"ssid_name": "ssid_open_2g_8", "appliedRadios": ["is2dot4GHz"], "vlan": 22},
                 {"ssid_name": "ssid_open_2g_9", "appliedRadios": ["is2dot4GHz"], "vlan": 23},
                 {"ssid_name": "ssid_open_2g_10", "appliedRadios": ["is2dot4GHz"], "vlan": 24},
                 {"ssid_name": "ssid_open_2g_11", "appliedRadios": ["is2dot4GHz"], "vlan": 25},
                 {"ssid_name": "ssid_open_2g_12", "appliedRadios": ["is2dot4GHz"], "vlan": 26},
                 {"ssid_name": "ssid_open_2g_13", "appliedRadios": ["is2dot4GHz"], "vlan": 27},
                 {"ssid_name": "ssid_open_2g_14", "appliedRadios": ["is2dot4GHz"], "vlan": 28},
                 ]},

    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
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
class Test2dotg8ssidUniqueValidVLAN(object):
    @pytest.mark.open
    def test_open_ssid_2g_7(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][0]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_2g_8(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][1]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_2g_9(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                            update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][2]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][2]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_2g_10(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][3]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][3]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_2g_11(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][4]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][4]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_2g_12(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][5]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][5]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_2g_13(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][6]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][6]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_2g_14(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][7]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "twog"
        vlan = setup_params_general["ssid_modes"]["open"][7]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_twog)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_twog, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_twog[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False


setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_5g_11", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 29},
                 {"ssid_name": "ssid_open_5g_12", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 30},
                 {"ssid_name": "ssid_open_5g_13", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 31},
                 {"ssid_name": "ssid_open_5g_14", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 32},
                 {"ssid_name": "ssid_open_5g_15", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 33},
                 {"ssid_name": "ssid_open_5g_16", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 34},
                 {"ssid_name": "ssid_open_5g_17", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 35},
                 {"ssid_name": "ssid_open_5g_18", "appliedRadios": ["is5GHz", "is5GHzL"], "vlan": 36},
                 ]},

    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
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
class Test5g8ssidUniqueValidVLAN(object):
    def test_open_ssid_5g_11(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][0]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_12(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][1]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_13(self, get_lanforge_data, lf_test, lf_tools, station_names_twog, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][2]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][2]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_14(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][3]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][3]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_15(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][4]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][4]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_16(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][5]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][5]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_17(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][6]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][6]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_18(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][7]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False


setup_params_general = {
    "mode": "VLAN",
    "ssid_modes": {
        "open": [{"ssid_name": "ssid_open_5g_19", "appliedRadios": ["is5GHzU", "is5GHz"], "vlan": 37},
                 {"ssid_name": "ssid_open_5g_20", "appliedRadios": ["is5GHzU", "is5GHz"], "vlan": 38},
                 {"ssid_name": "ssid_open_5g_21", "appliedRadios": ["is5GHzU", "is5GHz"], "vlan": 39},
                 {"ssid_name": "ssid_open_5g_22", "appliedRadios": ["is5GHzU", "is5GHz"], "vlan": 40},
                 {"ssid_name": "ssid_open_5g_23", "appliedRadios": ["is5GHzU", "is5GHz"], "vlan": 41},
                 {"ssid_name": "ssid_open_5g_24", "appliedRadios": ["is5GHzU", "is5GHz"], "vlan": 42},
                 {"ssid_name": "ssid_open_5g_25", "appliedRadios": ["is5GHzU", "is5GHz"], "vlan": 43},
                 {"ssid_name": "ssid_open_5g_26", "appliedRadios": ["is5GHzU", "is5GHz"], "vlan": 44},
                 ]},

    "rf": {},
    "radius": False
}


@pytest.mark.parametrize(
    'setup_profiles',
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
class Test5g8ssidUniqueValidVLAN(object):
    def test_open_ssid_5g_19(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][0]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][0]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_20(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][1]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][1]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_21(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][2]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][2]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_22(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][3]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][3]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_23(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][4]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        station_names = []
        for i in range(0, int(request.config.getini("num_stations"))):
            station_names.append(get_lanforge_data["lanforge_2dot4g_prefix"] + "0" + str(i))
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][4]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_24(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][5]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][5]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_25(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][6]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][6]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False

    def test_open_ssid_5g_26(self, get_lanforge_data, lf_test, lf_tools, station_names_fiveg, get_configuration,
                             update_report, test_cases):
        profile_data = setup_params_general["ssid_modes"]["open"][7]
        ssid_name = profile_data["ssid_name"]
        security_key = "[BLANK]"
        security = "open"
        mode = "VLAN"
        band = "fiveg"
        vlan = setup_params_general["ssid_modes"]["open"][7]["vlan"]
        lf_data = get_configuration["traffic_generator"]["details"]
        upstream_port = lf_data["upstream"]
        port_data = upstream_port.split('.')
        lf_test.Client_disconnect(station_names_fiveg)
        passes, result = lf_test.Client_Connectivity(ssid=ssid_name, security=security,
                                                     passkey=security_key, mode=mode, band=band,
                                                     station_name=station_names_fiveg, vlan_id=vlan)
        if result:
            sta_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                       port_data[1] + "/" + station_names_fiveg[0])["interface"]["ip"]
            sta_vlan_ip = lf_tools.json_get("/port/" + port_data[0] + "/" +
                                            port_data[1] + "/" + port_data[2])["interface"]["ip"]

            for m, n in zip(sta_ip[0:3], sta_vlan_ip[0:3]):
                if m != n:
                    assert False

            print("All stations got ip as per vlan")
            assert True
        else:
            assert False
