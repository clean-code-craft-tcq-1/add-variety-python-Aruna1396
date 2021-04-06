import unittest
import typewise_alert


class TypewiseTest(unittest.TestCase):

    def test_infers_breach_as_per_limits(self):
        self.assertTrue(typewise_alert.infer_breach(-20, 0, 35) == 'TOO_LOW')
        self.assertTrue(typewise_alert.infer_breach(120, 0, 45) == 'TOO_HIGH')
        self.assertTrue(typewise_alert.infer_breach(20, 0, 40) == 'NORMAL')

    def test_checks_input_data_valid(self):
        self.assertTrue(typewise_alert.is_input_valid('PASSIVE_COOLING', 120))
        self.assertFalse(typewise_alert.is_input_valid(None, -20))
        self.assertFalse(typewise_alert.is_input_valid(None, None))
        self.assertFalse(typewise_alert.is_input_valid('PASSIVE_COOLING', None))
        self.assertFalse(typewise_alert.is_input_valid('ULTRA_COOLING', 120))

    def test_checks_classify_temperature_breach_for_cooling_types(self):
        self.assertTrue(typewise_alert.classify_temperature_breach('coolingType', 120))

    def test_yields_alert_for_breaches(self):
        self.assertEqual(typewise_alert.check_and_alert('email', {'coolingType': 'PASSIVE_COOLING'}, 120), 'EMAIL_SENT')
        self.assertEqual(typewise_alert.check_and_alert('email', {'coolingType': 'HI_ACTIVE_COOLING'}, -20), 'EMAIL_SENT')
        self.assertEqual(typewise_alert.check_and_alert('controller', {'coolingType': 'MED_ACTIVE_COOLING'}, 90), 'CONTROLLER_ACTIVATED')


if __name__ == '__main__':
    unittest.main()
