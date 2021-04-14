import unittest
import typewise_alert
from mock import patch


class TypewiseTest(unittest.TestCase):

    def test_infers_breach_as_per_limits(self):
        self.assertEqual(typewise_alert.infer_breach(-20, 0, 35), 'TOO_LOW')
        self.assertEqual(typewise_alert.infer_breach(120, 0, 45), 'TOO_HIGH')
        self.assertEqual(typewise_alert.infer_breach(20, 0, 40), 'NORMAL')

    def test_checks_if_input_data_valid(self):
        self.assertTrue(typewise_alert.is_input_valid('PASSIVE_COOLING', 120))
        self.assertFalse(typewise_alert.is_input_valid(None, -20))
        self.assertFalse(typewise_alert.is_input_valid(None, None))
        self.assertFalse(typewise_alert.is_input_valid('MED_ACTIVE_COOLING', None))
        self.assertFalse(typewise_alert.is_input_valid('ULTRA_COOLING', 120))

    def test_checks_classify_temperature_breach_for_cooling_types(self):
        self.assertTrue(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 46) == 'TOO_HIGH')
        self.assertTrue(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', 41) == 'TOO_HIGH')
        self.assertTrue(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 36) == 'TOO_HIGH')
        self.assertTrue(typewise_alert.classify_temperature_breach(None, 36) == 'INVALID_INPUT')

    def test_compose_email_yields_right_mail_for_different_breach(self):
        breach_type = 'TOO_HIGH'
        email_content = {
            'To': typewise_alert.email_alert_message[breach_type]['recipient'],
            'Subject': "Breach Alert!!! Requesting Technician for corrective measures",
            'Body': typewise_alert.email_alert_message[breach_type]
        }
        self.assertEqual(typewise_alert.compose_email('TOO_HIGH'), email_content)
        self.assertNotEqual(typewise_alert.compose_email('TOO_LOW'), email_content)

    def test_check_and_alert_yields_apt_alerts_for_breaches(self):
        self.assertEqual(typewise_alert.check_and_alert('email', {'cooling_type': 'HI_ACTIVE_COOLING'}, -20),
                         'EMAIL_SENT')
        self.assertEqual(typewise_alert.check_and_alert('controller', {'cooling_type': 'MED_ACTIVE_COOLING'}, 90),
                         'CONTROLLER_ACTIVATED')
        self.assertEqual(typewise_alert.check_and_alert('controller', {'cooling_type': 'HI_ACTIVE_COOLING'}, 40),
                         'NORMAL')
        self.assertEqual(typewise_alert.check_and_alert('console', {'cooling_type': 'PASSIVE_COOLING'}, 140),
                         'CONSOLE_OUTPUT_SENT')

    # Using Mock functions only to test external components like email sending & Controller Actions

    @patch('controller_mailer_library.email_utility')
    def test_send_email_with_mock_email_utility_for_failure_scenario(self, mock_email_utility):
        mock_email_utility.return_value = 'EMAIL_ERROR'
        self.assertEqual(typewise_alert.send_email("TOO_LOW"), 'EMAIL_ERROR')

    @patch('controller_mailer_library.controller_utility')
    def test_send_to_controller_with_mock_controller_for_failure_scenario(self, mock_controller_utility):
        mock_controller_utility.return_value = 'CONTROLLER_ACTIVATION_ERROR'
        self.assertEqual(typewise_alert.send_to_controller("TOO_LOW"), 'CONTROLLER_ACTIVATION_ERROR')

    @patch('controller_mailer_library.email_utility')
    def test_check_and_alert_with_mock_email_utility_for_failure_scenario(self, mock_email_utility):
        mock_email_utility.return_value = 'EMAIL_ERROR'
        self.assertEqual(typewise_alert.check_and_alert('email', {'cooling_type': 'MED_ACTIVE_COOLING'}, -100),
                         'EMAIL_ERROR')

    @patch('controller_mailer_library.controller_utility')
    def test_send_to_controller_with_mock_controller_for_failure_scenario(self, mock_controller_utility):
        mock_controller_utility.return_value = 'CONTROLLER_ACTIVATION_ERROR'
        self.assertEqual(typewise_alert.check_and_alert('controller', {'cooling_type': 'PASSIVE_COOLING'}, 240),
                         'CONTROLLER_ACTIVATION_ERROR')


if __name__ == '__main__':
    unittest.main()
