import allure
import pytest

pytestmark = [pytest.mark.passpoint, pytest.mark.sanity, pytest.mark.eap]

setup_params_eap = {
    "mode": "BRIDGE",
    "ssid_modes": {
         "open": [
             {"ssid_name": "passpoint_profile_download", "appliedRadios": ["is2dot4GHz"]}
         ],
         "wpa2_eap": [
             {"ssid_name": "ssid_wpa2_eap_passpoint_2g", "appliedRadios": ["is2dot4GHz"]}
        ]
         #     {"ssid_name": "ssid_wpa2_eap_passpoint_5g", "appliedRadios": ["is5GHz"]}
         # ],
         # "wpa2_only_eap": [
         #     {"ssid_name": "ssid_wpa2_only_eap_passpoint_2g", "appliedRadios": ["is2dot4GHz"]},
         #     {"ssid_name": "ssid_wpa2_only_eap_passpoint_5g", "appliedRadios": ["is5GHz"]}
         # ]
    }
}


@pytest.mark.passpoint
@pytest.mark.eap
@pytest.mark.parametrize(
    'setup_profiles',
    [setup_params_eap],
    indirect=True,
    scope="class"
)
@pytest.mark.usefixtures("setup_profiles")
class TestNATModeEapAuth(object):

    def test_eap_passpoint_osu_id_provider_creation(self, setup_profiles):
        assert setup_profiles['passpoint_osu_id_provider']['sdk'], "Failed to create passpoint_osu_id_provider profile"

    def test_eap_passpoint_operator_creation(self, setup_profiles):
        assert setup_profiles['passpoint_operator_profile']['sdk']

    def test_eap_passpoint_venue_creation(self, setup_profiles):
        assert setup_profiles['passpoint_venue_profile']['sdk']

    def test_eap_passpoint_creation(self, setup_profiles):
        assert setup_profiles['passpoint']['sdk']

    def test_wpa2_eap_2g_ssid_profile_creation(self, setup_profiles):
        assert setup_profiles['ssid_wpa2_eap_passpoint_2g']['sdk'], "Failed to create ssid_wpa_eap_passpoint_2g " \
                                                                   "SSID profile"

    def test_wpa2_eap_2g_ssid_profile_vifc(self, setup_profiles):
        assert setup_profiles['ssid_wpa2_eap_passpoint_2g']['vifc'], "Failed to push ssid_wpa_eap_passpoint_2g" \
                                                                    " SSID profile to AP"

    def test_wpa2_eap_2g_ssid_profile_vifs(self, setup_profiles):
        assert setup_profiles['ssid_wpa2_eap_passpoint_2g']['vifs'], "Failed to apply ssid_wpa_eap_passpoint_2g" \
                                                                    " SSID profile to AP"

    @pytest.mark.wpa2_eap
    @pytest.mark.twog
    def test_wpa2_eap_2g(self, setup_profiles):
        print("Connect client to SSID")
        # SSID-1 "Name" to download the profile
        # SSID-2 "NAME" to verify if its avaiable in the wifi network
        # Need to profile name to remove



    #
    # @pytest.mark.wpa2_eap
    # @pytest.mark.fiveg
    # def test_wpa2_eap_5g(self, setup_profiles):
    #     print("Connect client to SSID")

    # @pytest.mark.wpa2_only_eap
    # @pytest.mark.twog
    # def test_wpa2_only_eap_2g(self, setup_profiles):
    #     print("Connect client to SSID")

    # @pytest.mark.wpa2_only_eap
    # @pytest.mark.fiveg
    # def test_wpa2_only_eap_5g(self, setup_profiles):
    #     print("Connect client to SSID")

