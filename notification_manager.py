from twilio.rest import Client
import smtplib
from dotenv.main import load_dotenv
import os

load_dotenv()

TWILIO_SID = os.environ['TWILIO_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_VIRTUAL_NUMBER = os.environ['TWILIO_VIRTUAL_NUMBER']
#TWILIO_VERIFIED_NUMBER = os.environ['TWILIO_VERIFIED_NUMBER']
EMAIL = os.environ['EMAIL']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

class NotificationManager:

    def __init__(self):
        notification_medium = ["print", "email", "sms"]
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        self.preferred_medium = notification_medium[1]

    def send_msg(self, message, lst_emails=[], lst_mobile_numbers=[]):
        if self.preferred_medium == "email":
            self.send_email(message, lst_emails)
        elif self.preferred_medium == "sms":
            self.send_sms(message, lst_mobile_numbers)
        else:
            print(message)

    def send_sms(self, message, lst_mobile_numbers):
        for nr in lst_mobile_numbers:
            message = self.client.messages.create(
                body=message,
                from_=TWILIO_VIRTUAL_NUMBER,
                to=nr,
            )
            # Prints if successfully sent.
            print(message.sid)

    def send_email(self, msg, lst_emails):
        msg = "Subject:Cheap Flight Notification\n\n" + msg

        connection = smtplib.SMTP("smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(user=EMAIL, password=EMAIL_PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=lst_emails, msg=msg)
        connection.close()
