import controller_mailer_library as lib

cooling_types_ranges = {
    "PASSIVE_COOLING": {'lower_limit': 0, 'upper_limit': 35},
    "MED_ACTIVE_COOLING": {'lower_limit': 0, 'upper_limit': 40},
    "HI_ACTIVE_COOLING": {'lower_limit': 0, 'upper_limit': 45},
}


email_alert_message = {"TOO_LOW": {'recipient': 'bmslowbreachalert@bosch.com',
                                   'alert': "Temperature is too low. Requesting immediate action"},
                       "TOO_HIGH": {'recipient': 'bmshighbreachalert@bosch.com',
                                    'alert': "Temperature is too high. Requesting immediate action"}
                       }


def check_and_alert(alert_target, battery_char, temperature_in_celsius):
    breach_type = \
        classify_temperature_breach(battery_char['cooling_type'], temperature_in_celsius)
    if breach_type != "NORMAL":
        return alert_target_type[alert_target](breach_type)
    else:
        return breach_type


def classify_temperature_breach(cooling_type, temperature_in_celsius):
    if is_input_valid(cooling_type, temperature_in_celsius):
        cooling_temp_range = cooling_types_ranges[cooling_type]
        return infer_breach(temperature_in_celsius, cooling_temp_range['lower_limit'], cooling_temp_range['upper_limit'])
    else:
        return 'INVALID_INPUT'


def is_input_valid(cooling_type, temperature_in_celsius):
    if cooling_type in cooling_types_ranges.keys() and temperature_in_celsius is not None:
        return True
    return False


def infer_breach(value, lower_limit, upper_limit):
    if value < lower_limit:
        return 'TOO_LOW'
    if value > upper_limit:
        return 'TOO_HIGH'
    return 'NORMAL'


def compose_email(breach_type):
    return {
        'To': email_alert_message[breach_type]['recipient'],
        'Subject': "Breach Alert!!! Requesting Technician for corrective measures",
        'Body': email_alert_message[breach_type]
    }


def send_email(email_data):
    return lib.email_utility(email_data)


def compose_and_send_email(breach_type):
    return send_email(compose_email(breach_type))


def send_to_controller(breach_type):
    return lib.controller_utility(breach_type)


def print_to_console(breach_type):
    print(f' Cooling temperature : {breach_type} \n \t Breach ALERT!!! Please take necessary corrective measures')
    return 'CONSOLE_OUTPUT_SENT'


alert_target_type = {
    'email': compose_and_send_email,
    'controller': send_to_controller,
    'console': print_to_console
}
