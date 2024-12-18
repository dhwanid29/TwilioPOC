import logging
import os
from dotenv import load_dotenv

load_dotenv()
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

logger = logging.getLogger(__name__)

class TwilioSMSClient:
    def __init__(self):
        self.client = TwilioSMSClient.create_client()
        self.default_sender = os.environ.get('TWILIO_DEFAULT_SENDER_NUMBER')

    @staticmethod
    def create_client():
        account_sid = os.environ.get('ACCOUNT_SID')
        auth_token = os.environ.get('AUTH_TOKEN')
        return Client(account_sid, auth_token)

    def send_text_message(self, to_number: str, body: str):
        try:
            self.client.messages.create(
                body=body,
                from_=self.default_sender,
                to=to_number
            )
        except (TwilioRestException, ConnectionError):
            logger.error('Connection error while sending SMS', exc_info=True)

        except Exception:
            logger.error('Error while sending SMS', exc_info=True)


sms_client = TwilioSMSClient()
sms_client.send_text_message(to_number="+918866445019", body="Kem choo")