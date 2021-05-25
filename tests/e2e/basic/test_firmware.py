"""
    Test Case Module:  setup test cases for basic test cases
    Details:    Firmware Upgrade

"""
import pytest

pytestmark = [pytest.mark.firmware, pytest.mark.sanity]


@pytest.mark.firmware_cloud
class TestFirmware(object):

    @pytest.mark.firmware_create
    def test_firmware_create(self, upload_firmware, update_report, test_cases):
        if upload_firmware != 0:
            update_report.update_testrail(case_id=test_cases["create_fw"],
                                          status_id=1,
                                          msg='Create new FW version by API successful')
            PASS = True
        else:
            update_report.update_testrail(case_id=test_cases["create_fw"],
                                          status_id=5,
                                          msg='Error creating new FW version by API')
            PASS = False
        assert PASS

    @pytest.mark.firmware_upgrade
    def test_firmware_upgrade_request(self, upgrade_firmware, update_report, test_cases):
        print()
        if not upgrade_firmware:
            update_report.update_testrail(case_id=test_cases["upgrade_api"],
                                          status_id=0,
                                          msg='Error requesting upgrade via API')
            PASS = False
        else:
            update_report.update_testrail(case_id=test_cases["upgrade_api"],
                                          status_id=1,
                                          msg='Upgrade request using API successful')
            PASS = True
        assert PASS

    @pytest.mark.check_active_firmware_cloud
    def test_active_version_cloud(self, get_latest_firmware, check_ap_firmware_cloud, update_report, test_cases):
        if get_latest_firmware != check_ap_firmware_cloud:
            update_report.update_testrail(case_id=test_cases["cloud_fw"],
                                          status_id=5,
                                          msg='CLOUDSDK reporting incorrect firmware version.')
        else:
            update_report.update_testrail(case_id=test_cases["cloud_fw"],
                                          status_id=1,
                                          msg='CLOUDSDK reporting correct firmware version.')

        assert get_latest_firmware == check_ap_firmware_cloud


@pytest.mark.firmware_ap
def test_ap_firmware(check_ap_firmware_ssh, get_latest_firmware, update_report,
                     test_cases):
    if check_ap_firmware_ssh == get_latest_firmware:
        update_report.update_testrail(case_id=test_cases["ap_upgrade"],
                                      status_id=1,
                                      msg='Upgrade to ' + str(get_latest_firmware) + ' successful')
    else:
        update_report.update_testrail(case_id=test_cases["ap_upgrade"],
                                      status_id=4,
                                      msg='Cannot reach AP after upgrade to check CLI - re-test required')

    assert check_ap_firmware_ssh == get_latest_firmware
