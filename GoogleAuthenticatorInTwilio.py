import os
import logging
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import pyqrcode

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Twilio2FA:
    """Twilio 2FA Client with Singleton Pattern and SMS Messaging"""
    _shared_client = None

    def __init__(self):
        if Twilio2FA._shared_client is None:
            account_sid = os.getenv("ACCOUNT_SID")
            auth_token = os.getenv("AUTH_TOKEN")
            Twilio2FA._shared_client = Client(account_sid, auth_token)

        self.client = Twilio2FA._shared_client
        self.default_sender = os.getenv("TWILIO_DEFAULT_SENDER_NUMBER")
        self.verify_service_sid = os.getenv("VERIFY_SERVICE_SID")

        logger.info(f"Twilio instance: {id(self)}")
        logger.info(f"Shared Twilio client: {id(Twilio2FA._shared_client)}")

    def create_qr_code(self, uri, filename="authenticator_code.png", scale=2):
        """Generate and save a QR code as an image."""
        try:
            qr_code = pyqrcode.create(uri)
            qr_code.png(filename, scale=scale)
            logger.info(f"QR code saved as {filename}")

        except Exception as e:
            logger.error(f"Error creating QR code: {e}", exc_info=True)

    def send_text_message(self, to_number: str, body: str):
        """Send a text message to the specified phone number."""
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

    def create_totp_factor(self, entity_id, friendly_name="Demo"):
        """Create a new TOTP factor for the given entity."""
        try:
            new_factor = self.client.verify.v2.services(self.verify_service_sid).entities(entity_id).new_factors.create(
                            friendly_name=friendly_name, factor_type="totp"
                        )
            logger.info(f"New factor created: {new_factor.sid}")
            return new_factor
        except Exception as e:
            logger.error(f"Error creating TOTP factor: {e}", exc_info=True)
            return None

    def verify_factor(self, entity_id, factor_sid, auth_payload):
        """Verify a TOTP factor with the provided payload."""
        try:
            factor = self.client.verify.v2.services(self.verify_service_sid).entities(entity_id).factors(factor_sid).update(auth_payload=auth_payload)
            logger.info(f"Factor verification status: {factor.status}")
            return factor.status
        except Exception as e:
            logger.error(f"Error verifying factor: {e}", exc_info=True)
            return None

if __name__ == "__main__":
    phone_number = input("Enter phone number: ")
    twilio_client = Twilio2FA()

    entity_id = "ff483d1ff591898a9942916050d2ca3f"
    new_factor = twilio_client.create_totp_factor(entity_id)

    if new_factor:
        twilio_client.create_qr_code(new_factor.binding.get('uri'))

        code = input("Enter the code: ")
        auth_payload = code
        status = twilio_client.verify_factor(entity_id, new_factor.sid, auth_payload)

        if status == "verified":
            twilio_client.send_text_message(phone_number, body="Hello")
