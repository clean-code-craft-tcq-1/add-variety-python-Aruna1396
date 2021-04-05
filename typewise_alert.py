cooling_types_ranges = {
    "PASSIVE_COOLING": {'lowerLimit': 0, 'upperLimit': 35},
    "MED_ACTIVE_COOLING": {'lowerLimit': 0, 'upperLimit': 40},
    "HI_ACTIVE_COOLING": {'lowerLimit': 0, 'upperLimit': 45},
}

email_alert_message = {"TOO_LOW": "Temperature is too low. Requesting immediate action",
                       "TOO_HIGH": "Temperature is too high. Requesting immediate action"
                       }

DEFAULT_HEADER_VALUE = 0xfeed


def check_and_alert(alert_target, battery_char, temperature_in_celsius):
    breach_type = \
        classify_temperature_breach(battery_char['coolingType'], temperature_in_celsius)
    if breach_type != "NORMAL":
        alert_target_type[alert_target](breach_type)


def classify_temperature_breach(cooling_type, temperature_in_celsius):
    if is_input_valid(cooling_type, temperature_in_celsius):
        lower_limit, upper_limit = cooling_types_ranges[cooling_type]
        return infer_breach(temperature_in_celsius, lower_limit, upper_limit)
    else:
        return 'INVALID_INPUT'


def is_input_valid(cooling_type, temperature_in_celsius):
    if cooling_type in cooling_types_ranges.keys() and temperature_in_celsius is None:
        return True
    return False


def infer_breach(value, lower_limit, upper_limit):
    if value < lower_limit:
        return 'TOO_LOW'
    if value > upper_limit:
        return 'TOO_HIGH'
    return 'NORMAL'


def send_to_controller(breach_type):
    header = DEFAULT_HEADER_VALUE
    print(f'{header}, {breach_type}')


def create_email(email_recipient):
    def send_email(breach_type):
        email_message = email_alert_message[breach_type]
        email_data = f"Dear,\n{email_recipient}\n \t {email_message}"
        print(email_data)
    return send_email


alert_target_type = {
    'email': create_email("bmstechnician@bosch.com"),
    'controller': send_to_controller
}
