import unittest
import typewise_alert
from unittest.mock import patch

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

    def test_compose_email_yield_right_mail_for_different_breach(self):
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
        self.assertEqual(typewise_alert.check_and_alert('console', {'cooling_type': 'HI_ACTIVE_COOLING'}, 140),
                         'CONSOLE_OUTPUT_SENT')


if __name__ == '__main__':
    unittest.main()
