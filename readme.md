# Twilio 2FA SMS Service

This project provides a simple implementation for sending and verifying OTPs (One-Time Passwords) and sending SMS messages using the Twilio API. The service can be used for two-factor authentication (2FA) and sending custom text messages.

---

## Features
- **Send OTP**: Generates and sends an OTP to a specified phone number via SMS.
- **Verify OTP**: Validates the OTP sent to the user's phone number.
- **Send Text Messages**: Sends custom text messages to a specified phone number.
- **Error Handling**: Includes logging and exception handling for reliable performance.

---

## Prerequisites

1. **Twilio Account**:
   - Sign up for a [Twilio account](https://www.twilio.com/).
   - Obtain the following credentials from the Twilio Console:
     - `ACCOUNT_SID`
     - `AUTH_TOKEN`
     - `TWILIO_DEFAULT_SENDER_NUMBER`
     - `VERIFY_SERVICE_SID`

2. **Python Environment**:
   - Python 3.8 or higher.
   - Install dependencies from `requirements.txt`.

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create a `.env` file in the project directory:
     ```env
     ACCOUNT_SID=your_account_sid
     AUTH_TOKEN=your_auth_token
     TWILIO_DEFAULT_SENDER_NUMBER=your_twilio_sender_number  # You need to purchase the number from twilio for sending messages. You can also buy any random number from twilio for trial purpose and replace it with your the desired number from which you wanted to send messages after buying the premium version.
     VERIFY_SERVICE_SID=your_verify_service_sid
     ```

---

## Usage

### 1. Send OTP
Use the `send_otp` method to send an OTP to a specified phone number.

```python
sms_client = Twilio2FASMSWithSingletonClient()
status = sms_client.send_otp(phone_number="+918488886809")
if status == "pending":
    print("OTP sent successfully.")
```

### 2. Verify OTP
Use the `verify_otp` method to validate the OTP sent to a user's phone number.

```python
verification_status = sms_client.verify_otp(phone_number="+918488886809", code="217740")
if verification_status == "approved":
    print("OTP verified successfully.")
```

### 3. Send Text Message
Use the `send_text_message` method to send a custom text message.

```python
sms_client.send_text_message(to_number="+918866445019", body="Kem choo")
```

---

## Logging

Logs are generated for key operations, including:
- Sending OTPs
- Verifying OTPs
- Sending text messages
- Error handling

Logs are printed to the console for easy debugging.

---

## Example

Here is a complete example:

```python
if __name__ == "__main__":
    phone_number = "+918488886809"
    sms_client = Twilio2FASMSWithSingletonClient()

    # Send OTP
    otp_status = sms_client.send_otp(phone_number)
    if otp_status == "pending":
        print("OTP sent successfully.")

    # Verify OTP
    verification_status = sms_client.verify_otp(phone_number, code="217740")
    if verification_status == "approved":
        print("OTP verified successfully.")

    # Send a text message
    sms_client.send_text_message(to_number="+918866445019", body="Kem choo")
```

---

## Dependencies
- Python
- `requests`
- `twilio`
- `python-dotenv`

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## Troubleshooting

### Common Issues

1. **Invalid Twilio Credentials**:
   - Ensure the `ACCOUNT_SID`, `AUTH_TOKEN`, and `VERIFY_SERVICE_SID` are correctly set in the `.env` file.

2. **Unverified Phone Numbers**:
   - Add your phone number in the Twilio Console for testing if your Twilio account is in trial mode.

3. **Network Issues**:
   - Check your internet connection if requests fail.

### Logging
Use the logs to diagnose issues. Errors are logged with detailed stack traces.

---

