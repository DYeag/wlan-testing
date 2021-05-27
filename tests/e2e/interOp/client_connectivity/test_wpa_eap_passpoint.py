import allure
import pytest


pytestmark = [pytest.mark.passpoint, pytest.mark.sanity, pytest.mark.enterprise]

setup_params_eap = {
    "mode": "NAT",
    "ssid_modes": {
        "wpa_eap": [
            {"ssid_name": "ssid_wpa_eap_passpoint_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa_eap_passpoint_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa2_eap": [
            {"ssid_name": "ssid_wpa2_eap_passpoint_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa2_eap_passpoint_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}],
        "wpa2_only_eap": [
            {"ssid_name": "ssid_wpa3_eap_passpoint_2g", "appliedRadios": ["is2dot4GHz"]},
            {"ssid_name": "ssid_wpa3_eap_passpoint_5g", "appliedRadios": ["is5GHzU", "is5GHz", "is5GHzL"]}]
    }
}


@pytest.mark.passpoint
@pytest.mark.enterprise
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_eap],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestNATModeEapAuth(object):

    @pytest.mark.wpa_eap
    @pytest.mark.twog
    def test_wpa_eap_2g(self, station_names_twog, setup_profiles, get_lanforge_data, lf_test, update_report,
                               test_cases, radius_info):
        print("Connect client to SSID")
