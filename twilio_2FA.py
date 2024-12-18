# import json
# import logging
# import os
#
# import requests
# from dotenv import load_dotenv
#
# load_dotenv()
# from twilio.base.exceptions import TwilioRestException
# from twilio.rest import Client
#
# logger = logging.getLogger(__name__)
#
# class Twilio2FASMS:
#     def __init__(self):
#         self.account_sid = os.environ.get('ACCOUNT_SID')
#         self.auth_token = os.environ.get('AUTH_TOKEN')
#         self.default_sender = os.environ.get('TWILIO_DEFAULT_SENDER_NUMBER')
#         self.client = Twilio2FASMS.create_client()
#
#     @staticmethod
#     def create_client():
#         account_sid = os.environ.get('ACCOUNT_SID')
#         auth_token = os.environ.get('AUTH_TOKEN')
#         return Client(account_sid, auth_token)
#
#     def send_otp(self):
#         verification_url = f'https://verify.twilio.com/v2/Services/{"VA353b3f910d1b7a881aa3e32b7dcb7fad"}/Verifications'
#         print(verification_url)
#         account_sid = self.create_client()
#         print(account_sid, 'HIHI')
#         data = {
#             "To": "+918488886809",  # Replace with the phone number to verify
#             "Channel": "sms"  # The channel (e.g., sms, call)
#         }
#         auth = (self.account_sid, self.auth_token)
#         print(verification_url)
#         send_otp = requests.post(verification_url, data=data, auth=auth)
#         print(json.loads(send_otp.text), 'HEY')
#         return json.loads(send_otp.text).get('status')
#
#     def verify_otp(self):
#         code_verification_url = f'https://verify.twilio.com/v2/Services/VA353b3f910d1b7a881aa3e32b7dcb7fad/VerificationCheck'
#         data = {
#             "To": "+918488886809",  # Replace with the phone number to verify
#             "Code": "217740"  # The code
#         }
#         auth = (self.account_sid, self.auth_token)
#         verify_otp = requests.post(code_verification_url, data=data, auth=auth)
#         print(verify_otp.text, 'HEYAA')
#         return json.loads(verify_otp.text).get('status')
#
#     def send_text_message(self, to_number: str, body: str):
#         try:
#             if self.verify_otp() == 'approved':
#                 print('OTP approved')
#
#             self.client.messages.create(
#                 body=body,
#                 from_=self.default_sender,
#                 to=to_number
#             )
#         except (TwilioRestException, ConnectionError):
#             logger.error('Connection error while sending SMS', exc_info=True)
#
#         except Exception:
#             logger.error('Error while sending SMS', exc_info=True)
#
#
# sms_client = Twilio2FASMS()
# sms_client.send_text_message(to_number="+918866445019", body="Kem choo")



import json
import logging
import os

import requests
from dotenv import load_dotenv
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

load_dotenv()

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Twilio2FASMS:
    def __init__(self):
        self.account_sid = os.getenv('ACCOUNT_SID')
        self.auth_token = os.getenv('AUTH_TOKEN')
        self.default_sender = os.getenv('TWILIO_DEFAULT_SENDER_NUMBER')
        self.verify_service_sid = os.getenv('VERIFY_SERVICE_SID')# Twilio Verify Service SID
        self.client = self._create_client()

    def _create_client(self):
        """Create and return a Twilio client."""
        return Client(self.account_sid, self.auth_token)

    def send_otp(self, phone_number: str, channel: str = "sms"):
        """Send an OTP to the given phone number."""
        url = f'https://verify.twilio.com/v2/Services/{self.verify_service_sid}/Verifications'
        data = {"To": phone_number, "Channel": channel}
        auth = (self.account_sid, self.auth_token)

        try:
            response = requests.post(url, data=data, auth=auth)
            response.raise_for_status()
            print(response.text, 'SO')
            status = response.json().get('status')
            logger.info(f"OTP sent to {phone_number}, status: {status}")
            return status
        except requests.RequestException as e:
            logger.error(f"Error sending OTP: {e}")
            return None

    def verify_otp(self, phone_number: str, code: str):
        """Verify the OTP for the given phone number."""
        url = f'https://verify.twilio.com/v2/Services/{self.verify_service_sid}/VerificationCheck'
        data = {"To": phone_number, "Code": code}
        auth = (self.account_sid, self.auth_token)

        try:
            response = requests.post(url, data=data, auth=auth)
            response.raise_for_status()
            status = response.json().get('status')
            logger.info(f"OTP verification for {phone_number}, status: {status}")
            return status
        except requests.RequestException as e:
            logger.error(f"Error verifying OTP: {e}")
            return None

    def send_text_message(self, to_number: str, body: str):
        """Send a text message to the given phone number."""
        try:
            self.client.messages.create(body=body, from_=self.default_sender, to=to_number)
            logger.info(f"Message sent to {to_number}")
        except TwilioRestException as e:
            logger.error(f"Error sending SMS: {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending SMS: {e}", exc_info=True)


if __name__ == "__main__":
    phone_number = input("Enter your phone number: ")
    sms_client = Twilio2FASMS()

    # Send OTP
    otp_status = sms_client.send_otp(phone_number)
    if otp_status == "pending":
        logger.info("OTP sent successfully.")
        code = input("Enter OTP: ")
    else:
        code = None

    # Verify OTP
    verification_status = sms_client.verify_otp(phone_number, code=code)
    if verification_status == "approved":
        sms_client.send_text_message(phone_number, body="Hello")
