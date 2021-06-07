import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)
if "libs" not in sys.path:
    sys.path.append(f"../libs")

import time
import pytest
import allure
from collections import defaultdict
from lanforge.lf_tests import RunTest
from configuration import PASSPOINT_PROVIDER_INFO
from configuration import PASSPOINT_OPERATOR_INFO
from configuration import PASSPOINT_VENUE_INFO
from configuration import PASSPOINT_PROFILE_INFO
from controller.controller import ProfileUtility
#from configuration import PASSPOINT_CONFIG

@pytest.fixture(scope="session")
def setup_vlan():
    vlan_id = [100]
    allure.attach(body=str(vlan_id), name="VLAN Created: ")
    yield vlan_id[0]

@pytest.fixture(scope="session")
def instantiate_profile():
    yield ProfileUtility


@allure.feature("PASSPOINT CONNECTIVITY SETUP")
@pytest.fixture(scope="class")
def setup_profiles(request, setup_controller, testbed, setup_vlan, get_equipment_id,
                   instantiate_profile, get_markers, passpoint_provider_info, passpoint_operator_info,
                    passpoint_venue_info, passpoint_profile_info,
                   get_configuration, radius_info, radius_accounting_info, get_apnos):
    instantiate_profile = instantiate_profile(sdk_client=setup_controller)
    vlan_id, mode = 0, 0
    instantiate_profile.cleanup_objects()
    parameter = dict(request.param)
    test_cases = {}
    profile_data = {}
    if parameter["mode"] not in ["BRIDGE", "NAT", "VLAN"]:
        print("Invalid Mode: ", parameter["mode"])
        allure.attach(body=parameter["mode"], name="Invalid Mode: ")
        yield test_cases

    if parameter["mode"] == "NAT":
        mode = "NAT"
        vlan_id = 1
    if parameter["mode"] == "BRIDGE":
        mode = "BRIDGE"
        vlan_id = 1
    if parameter["mode"] == "VLAN":
        mode = "BRIDGE"
        vlan_id = setup_vlan

    ap_profile = testbed + "-Equipment-AP-" + parameter["mode"]
    instantiate_profile.delete_profile_by_name(profile_name=ap_profile)
    profile_data["equipment_ap"] = {"profile_name": ap_profile}
    profile_data["ssid"] = {}
    # Only passpoint SSID need to be applied with passpoint profiles leaving ssid used for
    # profile download - passpoint_profile_download
    profile_data["allowed_ssids"] = []
    for i in parameter["ssid_modes"]:
        profile_data["ssid"][i] = []
        for j in range(len(parameter["ssid_modes"][i])):
            profile_name = testbed + "-SSID-" + i + "-" + str(j) + "-" + parameter["mode"]
            data = parameter["ssid_modes"][i][j]
            data["profile_name"] = profile_name
            if "mode" not in dict(data).keys():
                data["mode"] = mode
            if "vlan" not in dict(data).keys():
                data["vlan"] = vlan_id
            instantiate_profile.delete_profile_by_name(profile_name=profile_name)
            profile_data["ssid"][i].append(data)

    instantiate_profile.delete_profile_by_name(profile_name=testbed + "-Automation-Radius-Profile-" + mode)
    time.sleep(10)

    # RF Profile Creation
    rf_profile_data = {
        "name": testbed + "-RF-Profile-" + parameter["mode"] + "-" + get_configuration["access_point"][0]["mode"]
    }
    try:
        instantiate_profile.delete_profile_by_name(profile_name=rf_profile_data["name"])
        rf_profile_data = instantiate_profile.set_rf_profile(profile_data=rf_profile_data,
                                           mode=get_configuration["access_point"][0]["mode"])
        allure.attach(body=str(rf_profile_data),
                      name="RF Profile Created : " + get_configuration["access_point"][0]["mode"])
    except Exception as e:
        print(e)
        allure.attach(body=str(e), name="Exception ")

    # Radius Profile Creation
    radius_info = radius_info
    radius_info["name"] = testbed + "-Automation-Radius-Profile"
    instantiate_profile.delete_profile_by_name(profile_name=testbed + "-Automation-Radius-Profile" )
    try:
        instantiate_profile.create_radius_profile(radius_info=radius_info, radius_accounting_info=radius_accounting_info)
        test_cases["radius_profile"] = True
        allure.attach(body=str(radius_info), name="Radius Profile Created")
    except Exception as e:
        print(e)
        test_cases["radius_profile"] = False

    # SSID Profile Creation
    for mode in profile_data["ssid"]:
        if mode == "open":
            for j in profile_data["ssid"][mode]:
                try:
                    if "is2dot4GHz" in list(j["appliedRadios"]):
                        creates_profile = instantiate_profile.create_open_ssid_profile(profile_data=j)
                        test_cases[j["ssid_name"]] = {"sdk": True}
                        allure.attach(body=str(creates_profile), name="SSID Profile Created")
                except Exception as e:
                    print(e)
                    test_cases[j["ssid_name"]] = {"sdk": False}
                    allure.attach(body=str(e), name="SSID Profile Creation Failed")
        if mode == "wpa_eap":
            for j in profile_data["ssid"][mode]:
                if mode in get_markers.keys() and get_markers[mode]:
                    try:
                        if "twog" in get_markers.keys() and get_markers["twog"] and "is2dot4GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa_eap_passpoint_ssid_profile(profile_data=j)
                            profile_data["allowed_ssids"].append(creates_profile._id)
                            test_cases[j["ssid_name"]] = {"sdk": True}
                            allure.attach(body=str(creates_profile), name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases[j["ssid_name"]] = {"sdk": False}
                        allure.attach(body=str(e), name="SSID Profile Creation Failed")
                    try:
                        if "fiveg" in get_markers.keys() and get_markers["fiveg"] and "is5GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa_eap_passpoint_ssid_profile(profile_data=j)
                            profile_data["allowed_ssids"].append(creates_profile._id)
                            test_cases[j["ssid_name"]] = {"sdk": True}
                            allure.attach(body=str(creates_profile), name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases[j["wpa_eap_5g"]] = {"sdk": False}
                        allure.attach(body=str(e), name="SSID Profile Creation Failed")
        if mode == "wpa2_eap":
            for j in profile_data["ssid"][mode]:
                if mode in get_markers.keys() and get_markers[mode]:
                    try:
                        if "twog" in get_markers.keys() and get_markers["twog"] and "is2dot4GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa2_eap_passpoint_ssid_profile(profile_data=j)
                            profile_data["allowed_ssids"].append(creates_profile._id)
                            test_cases[j["ssid_name"]] = {"sdk": True}
                            allure.attach(body=str(creates_profile), name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases[j["ssid_name"]] = {"sdk": False}
                        allure.attach(body=str(e), name="SSID Profile Creation Failed")
                    try:
                        if "fiveg" in get_markers.keys() and get_markers["fiveg"] and "is5GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa2_eap_passpoint_ssid_profile(profile_data=j)
                            profile_data["allowed_ssids"].append(creates_profile._id)
                            test_cases[j["ssid_name"]] = {"sdk": True}
                            allure.attach(body=str(creates_profile), name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases[j["ssid_name"]] = {"sdk": False}
                        allure.attach(body=str(e), name="SSID Profile Creation Failed")
        if mode == "wpa2_only_eap":
            for j in profile_data["ssid"][mode]:
                if mode in get_markers.keys() and get_markers[mode]:
                    try:
                        if "twog" in get_markers.keys() and get_markers["twog"] and "is2dot4GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa2_only_eap_passpoint_ssid_profile(profile_data=j)
                            profile_data["allowed_ssids"].append(creates_profile._id)
                            test_cases[j["ssid_name"]] = {"sdk": True}
                            allure.attach(body=str(creates_profile), name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases[j["ssid_name"]] = {"sdk": False}
                        allure.attach(body=str(e), name="SSID Profile Creation Failed")
                    try:
                        if "fiveg" in get_markers.keys() and get_markers["fiveg"] and "is5GHz" in list(
                                j["appliedRadios"]):
                            creates_profile = instantiate_profile.create_wpa2_only_eap_passpoint_ssid_profile(profile_data=j)
                            profile_data["allowed_ssids"].append(creates_profile._id)
                            test_cases[j["ssid_name"]] = {"sdk": True}
                            allure.attach(body=str(creates_profile), name="SSID Profile Created")
                    except Exception as e:
                        print(e)
                        test_cases[j["ssid_name"]] = {"sdk": False}
                        allure.attach(body=str(e), name="SSID Profile Creation Failed")

    # Passpoint OSU ID provider profile creation
    passpoint_provider_info = passpoint_provider_info
    test_cases["passpoint_osu_id_provider"] = dict()
    profile_name = testbed + "-Automation-Passpoint-OSU-ID-Provider-Profile"
    passpoint_provider_info["profile_name"] = profile_name
    instantiate_profile.delete_profile_by_name(profile_name=profile_name)
    try:
        creates_profile = instantiate_profile.create_passpoint_osu_id_provider_profile(profile_data=passpoint_provider_info)
        allure.attach(body=str(creates_profile), name="Passpoint OSU ID provider Profile Created")
        test_cases["passpoint_osu_id_provider"] = {"sdk": True}
    except Exception as e:
        print(e)
        test_cases["passpoint_osu_id_provider"] = {"sdk": False}
        allure.attach(body=str(e), name="Passpoint OSU ID provider Profile Creation Failed")

    # Passpoint operator profile creation
    test_cases["passpoint_operator_profile"] = dict()
    passpoint_operator_info = passpoint_operator_info
    profile_name = testbed + "-Automation-Passpoint-Operator-Profile"
    passpoint_operator_info["profile_name"] = profile_name
    instantiate_profile.delete_profile_by_name(profile_name=profile_name)
    try:
        creates_profile = instantiate_profile.create_passpoint_operator_profile(profile_data=passpoint_operator_info)
        allure.attach(body=str(creates_profile), name="Passpoint Operator Profile Created")
        test_cases["passpoint_operator_profile"] = {"sdk": True}
        profile_data["passpoint_operator"] = profile_name
    except Exception as e:
        print(e)
        test_cases["passpoint_operator_profile"] = {"sdk": False}
        allure.attach(body=str(e), name="Passpoint Operator Profile Creation Failed")

    # Passpoint Venue profile creation
    passpoint_venue_info = passpoint_venue_info
    test_cases["passpoint_venue_profile"] = dict()
    profile_name = testbed + "-Automation-Passpoint-Venue-Profile"
    passpoint_venue_info["profile_name"] = profile_name
    instantiate_profile.delete_profile_by_name(profile_name=profile_name)
    try:
        creates_profile = instantiate_profile.create_passpoint_venue_profile(profile_data=passpoint_venue_info)
        allure.attach(body=str(creates_profile), name="Passpoint Venue Profile Created")
        test_cases["passpoint_venue_profile"] = {"sdk": True}
        profile_data["passpoint_venue"] = profile_name
    except Exception as e:
        print(e)
        test_cases["passpoint_venue"] = {"sdk": False}
        allure.attach(body=str(e), name="Passpoint Venue Profile Creation Failed")

    # Passpoint profile creation
    passpoint_profile_info = passpoint_profile_info
    profile_name = testbed + "-Automation-Passpoint-Profile"
    passpoint_profile_info["profile_name"] = profile_name
    passpoint_profile_info["allowed_ssids"] = profile_data["allowed_ssids"]
    instantiate_profile.delete_profile_by_name(profile_name=profile_name)
    try:
        creates_profile = instantiate_profile.create_passpoint_profile(profile_data=passpoint_profile_info)
        allure.attach(body=str(creates_profile), name="Passpoint Profile Created")
        test_cases["passpoint"] = {"sdk": True}
        profile_data["passpoint"] = profile_name
    except Exception as e:
        print(e)
        test_cases["passpoint"] = {"sdk": False}
        allure.attach(body=str(e), name="Passpoint Profile Creation Failed")

    # Update SSID profile with passpoint config
    passpoint_profile_info = passpoint_profile_info
    for ssid_profile in profile_data["ssid"].keys():
        for ssid in profile_data["ssid"][ssid_profile]:
            if ssid["ssid_name"] == "passpoint_profile_download":
                continue
            allure.attach(body=str(ssid), name="Updating SSID profile")
            passpoint_profile_info["ssid_profile_name"] = ssid["profile_name"]
            instantiate_profile.update_ssid_profile(profile_info=passpoint_profile_info)

    # Equipment AP Profile Creation
    try:
        instantiate_profile.set_ap_profile(profile_data=profile_data["equipment_ap"])
        test_cases["quipment_ap"] = {"sdk": True}
        allure.attach(body=str(profile_data["equipment_ap"]), name="Equipment AP Profile Created")
    except Exception as e:
        print(e)
        test_cases["equipment_ap"] = {"sdk": False}
        allure.attach(body=str(e), name="Equipment AP Profile Creation Failed")

    # Push the Equipment AP Profile to AP
    try:
        for i in get_equipment_id:
            instantiate_profile.push_profile_old_method(equipment_id=i)
    except Exception as e:
        print(e)
        print("failed to create AP Profile")

    print("Waiting for profiles to be pushed to AP")
    time.sleep(230)

    # Check the VIF Config and VIF State of SSIDs
    ap_ssh = get_apnos(get_configuration["access_point"][0], pwd="../libs/apnos/")
    vifc_ssids = list(ap_ssh.get_vif_config_ssids())
    print(vifc_ssids)
    vifs_ssids = list(ap_ssh.get_vif_state_ssids())
    print(vifs_ssids)
    for i in instantiate_profile.profile_creation_ids["ssid"]:
        ssid = instantiate_profile.get_ssid_name_by_profile_id(profile_id=i)
        test_cases[ssid]["vifc"] = True if ssid in vifc_ssids else False
        test_cases[ssid]["vifs"] = True if ssid in vifs_ssids else False
    print("============ Test status ======\n", test_cases)

    def teardown_session():
        print("\nRemoving Profiles")
        instantiate_profile.delete_profile_by_name(profile_name=profile_data['equipment_ap']['profile_name'])
        instantiate_profile.delete_profile(instantiate_profile.profile_creation_ids["ssid"])
        instantiate_profile.delete_profile(instantiate_profile.profile_creation_ids["radius"])
        instantiate_profile.delete_profile(instantiate_profile.profile_creation_ids["rf"])
        instantiate_profile.delete_profile(instantiate_profile.profile_creation_ids["passpoint_osu_id_provider"])
        instantiate_profile.delete_profile(instantiate_profile.profile_creation_ids["passpoint_operator"])
        instantiate_profile.delete_profile(instantiate_profile.profile_creation_ids["passpoint_venue"])
        instantiate_profile.delete_profile(instantiate_profile.profile_creation_ids["passpoint"])
        allure.attach(body=str(profile_data['equipment_ap']['profile_name'] + "\n"),
                      name="Tear Down in Profiles ")
        time.sleep(20)

    request.addfinalizer(teardown_session)
    yield test_cases


@pytest.fixture(scope="session")
def passpoint_provider_info():
    allure.attach(body=str(PASSPOINT_PROVIDER_INFO), name="Passpoint Provider Info: ")
    yield PASSPOINT_PROVIDER_INFO


@pytest.fixture(scope="session")
def passpoint_operator_info():
    allure.attach(body=str(PASSPOINT_OPERATOR_INFO), name="Passpoint operator Info: ")
    yield PASSPOINT_OPERATOR_INFO


@pytest.fixture(scope="session")
def passpoint_venue_info():
    allure.attach(body=str(PASSPOINT_VENUE_INFO), name="Passpoint venue Info: ")
    yield PASSPOINT_VENUE_INFO


@pytest.fixture(scope="session")
def passpoint_profile_info():
    allure.attach(body=str(PASSPOINT_PROFILE_INFO), name="Passpoint profile Info: ")
    yield PASSPOINT_PROFILE_INFO

