import os
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM_PHONE = os.environ.get("TWILIO_FROM_PHONE")
TWILIO_VIRTUAL_PHONE = os.environ.get("TWILIO_VIRTUAL_PHONE")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
message = client.messages.create(
    from_=TWILIO_FROM_PHONE,
    body='hello world',
    to=TWILIO_VIRTUAL_PHONE
)
print("sid:" + message.sid)
print("From: " + message.from_)
print("To: " + message.to)
print("body: " + message.body)
print("status: " + message.status)
print(f"price: {message.price if message.price else 'N/A'}")
print(
    f"error_message: {message.error_message if message.error_message else 'N/A'}")
