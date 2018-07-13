__author__ = 'osito_wang'
__date__ = '2018/6/19 15:40'
from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from Mooc_Online.settings import EMAIL_FROM


# Send the email with link for register and forget password
def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    # create the random verify code
    if send_type == "update":
        random_str = generate_random_str(4)
    else:
        random_str = generate_random_str(16)
    # Assign values to the model
    email_record.code = random_str
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""
    # send the register verifying email
    if send_type == "register":
        email_title = "Activate your Mooc_Online Account"
        email_body = "Please click the below link to activate your account" \
                     "Mooc_Online account: http://127.0.0.1:8000/activate/{0}".format(random_str)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "Reset your Mooc_Online Password"
        email_body = "Please click the below link to reset your password " \
                     "Mooc_Online account: http://127.0.0.1:8000/reset/{0}".format(random_str)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "update":
        email_title = "Change your Mooc_Online Account Email"
        email_body = "This is your email update verify code:{0}".format(random_str)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


def generate_random_str(random_length=8):
    code_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        code_str += chars[random.randint(0, length)]
    return code_str
