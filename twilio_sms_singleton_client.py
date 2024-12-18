# import json
# import logging
# import os
#
# import requests
# from dotenv import load_dotenv
# from twilio.base.exceptions import TwilioRestException
# from twilio.rest import Client
#
# load_dotenv()
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
#
# class TwilioClientSingleton:
#     """A Singleton class for the Twilio Client."""
#     _instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             cls._instance._initialize(*args, **kwargs)
#         return cls._instance
#
#     def _initialize(self, account_sid, auth_token):
#         self.client = Client(account_sid, auth_token)
#
# class Twilio2FASMSWithSingletonClient:
#     def __init__(self):
#         self.account_sid = os.getenv('ACCOUNT_SID')
#         self.auth_token = os.getenv('AUTH_TOKEN')
#         self.default_sender = os.getenv('TWILIO_DEFAULT_SENDER_NUMBER')
#         self.verify_service_sid = os.getenv('VERIFY_SERVICE_SID')  # Twilio Verify Service SID
#         self.client = TwilioClientSingleton(self.account_sid, self.auth_token).client
#
#     def send_otp(self, phone_number: str, channel: str = "sms"):
#         """Send an OTP to the given phone number."""
#         url = f'https://verify.twilio.com/v2/Services/{self.verify_service_sid}/Verifications'
#         data = {"To": phone_number, "Channel": channel}
#         auth = (self.account_sid, self.auth_token)
#
#         try:
#             response = requests.post(url, data=data, auth=auth)
#             response.raise_for_status()
#             print(response.text, 'SO')
#             status = response.json().get('status')
#             logger.info(f"OTP sent to {phone_number}, status: {status}")
#             return status
#         except requests.RequestException as e:
#             logger.error(f"Error sending OTP: {e}")
#             return None
#
#     def verify_otp(self, phone_number: str, code: str):
#         """Verify the OTP for the given phone number."""
#         url = f'https://verify.twilio.com/v2/Services/{self.verify_service_sid}/VerificationCheck'
#         data = {"To": phone_number, "Code": code}
#         auth = (self.account_sid, self.auth_token)
#
#         try:
#             response = requests.post(url, data=data, auth=auth)
#             response.raise_for_status()
#             status = response.json().get('status')
#             logger.info(f"OTP verification for {phone_number}, status: {status}")
#             return status
#         except requests.RequestException as e:
#             logger.error(f"Error verifying OTP: {e}")
#             return None
#
#     def send_text_message(self, to_number: str, body: str):
#         """Send a text message to the given phone number."""
#         try:
#             self.client.messages.create(body=body, from_=self.default_sender, to=to_number)
#             logger.info(f"Message sent to {to_number}")
#         except TwilioRestException as e:
#             logger.error(f"Error sending SMS: {e}")
#         except Exception as e:
#             logger.error(f"Unexpected error sending SMS: {e}", exc_info=True)
#
#
# if __name__ == "__main__":
#     phone_number = "+918488886809"
#     sms_client = Twilio2FASMSWithSingletonClient()
#
#     # Send OTP
#     otp_status = sms_client.send_otp(phone_number)
#     if otp_status == "pending":
#         logger.info("OTP sent successfully.")
#         code = input("Enter OTP: ")
#     else:
#         code = None
#
#     # Verify OTP
#     verification_status = sms_client.verify_otp(phone_number, code=code)
#     if verification_status == "approved":
#         sms_client.send_text_message(phone_number, body="Hello")



import os
import logging
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import requests

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Twilio2FASMSWithSingletonClient:
    """Twilio SMS Client for 2FA with singleton cleint and custom SMS messages."""
    shared_client = None

    def __init__(self):
        if Twilio2FASMSWithSingletonClient.shared_client is None:
            # Initialize the Twilio client once and store it in a class variable
            account_sid = os.getenv("ACCOUNT_SID")
            auth_token = os.getenv("AUTH_TOKEN")
            Twilio2FASMSWithSingletonClient.shared_client = Client(account_sid, auth_token)

        self.client = Twilio2FASMSWithSingletonClient.shared_client
        self.default_sender = os.getenv("TWILIO_DEFAULT_SENDER_NUMBER")
        self.verify_service_sid = os.getenv("VERIFY_SERVICE_SID")
        print(f"Twilio instance: {id(self)}")
        logger.info(f"Twilio instance: {id(self)}")
        print(f"Shared Twilio client: {id(Twilio2FASMSWithSingletonClient.shared_client)}")
        logger.info(f"Shared Twilio client: {id(Twilio2FASMSWithSingletonClient.shared_client)}")

    def send_otp(self, phone_number: str, channel: str = "sms"):
        """Send an OTP to the given phone number."""
        url = f'https://verify.twilio.com/v2/Services/{self.verify_service_sid}/Verifications'
        data = {"To": phone_number, "Channel": channel}
        auth = (os.getenv("ACCOUNT_SID"), os.getenv("AUTH_TOKEN"))

        try:
            response = requests.post(url, data=data, auth=auth)
            response.raise_for_status()
            status = response.json().get("status")
            logger.info(f"OTP sent to {phone_number}, status: {status}")
            return status
        except requests.RequestException as e:
            logger.error(f"Error sending OTP: {e}")
            return None

    def verify_otp(self, phone_number: str, code: str):
        """Verify the OTP for the given phone number."""
        url = f'https://verify.twilio.com/v2/Services/{self.verify_service_sid}/VerificationCheck'
        data = {"To": phone_number, "Code": code}
        auth = (os.getenv("ACCOUNT_SID"), os.getenv("AUTH_TOKEN"))

        try:
            response = requests.post(url, data=data, auth=auth)
            response.raise_for_status()
            status = response.json().get("status")
            logger.info(f"OTP verification for {phone_number}, status: {status}")
            return status
        except requests.RequestException as e:
            logger.error(f"Error verifying OTP: {e}")
            return None

    def send_text_message(self, to_number: str, body: str):
        """Send a text message to the given phone number."""
        try:
            self.client.messages.create(
                body=body,
                from_=self.default_sender,
                to=to_number
            )
            logger.info(f"Message sent to {to_number}")
        except TwilioRestException as e:
            logger.error(f"Error sending SMS: {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending SMS: {e}", exc_info=True)


if __name__ == "__main__":
    sms_client_1 = Twilio2FASMSWithSingletonClient()
    sms_client_2 = Twilio2FASMSWithSingletonClient()

    # Compare the instance of shared_client
    if sms_client_1.client is sms_client_2.client:
        print("Singleton pattern is working. Both clients are the same.")
        logger.info("Singleton pattern is working. Both clients are the same.")
    else:
        print("Singleton pattern is NOT working. Clients are different.")
        logger.warning("Singleton pattern is NOT working. Clients are different.")

    phone_number = input("Enter phone number: ")
    sms_client = Twilio2FASMSWithSingletonClient()

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
