controller_action = {"TOO_LOW": 'HEATER_ON',
                     "TOO_HIGH": 'COOLER_ON'}


def email_utility(email_data):
    # This dummy email utility to be replaced with actual one in real cases
    print(email_data)
    return "EMAIL_SENT"


def controller_utility(breach_type):
    # controller sending utility to be added in real use case
    corrective_action = controller_action[breach_type]
    controller_log = f' Battery Temperature {breach_type} : {corrective_action} \n \tController Activated'
    print(controller_log)
    return "CONTROLLER_ACTIVATED"
