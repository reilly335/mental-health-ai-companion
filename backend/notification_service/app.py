# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from twilio.rest import Client
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

app = Flask(__name__)
CORS(app)

# Twilio configuration
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN  = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# SendGrid configuration
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
sendgrid_client = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

@app.route('/notify', methods=['POST'])
def notify():
    """
    Send notification to user or professional via SMS or Email.

    Expected JSON payload:
    {
        "type": "sms" or "email",
        "recipient": "+1234567890" or "user@example.com",
        "subject": "Notification Subject", (optional, for email)
        "message": "Your notification message"
    }
    """
    data = request.get_json()
    notification_type = data.get('type')
    recipient = data.get('recipient')
    message = data.get('message')
    subject = data.get('subject', 'MH-AI Notification')

    if not notification_type or not recipient or not message:
        return jsonify({'message': 'Type, recipient, and message are required'}), 400

    try:
        if notification_type == 'sms':
            send_sms(recipient, message)
        elif notification_type == 'email':
            send_email(recipient, subject, message)
        else:
            return jsonify({'message': 'Invalid notification type'}), 400

        return jsonify({'status': 'sent'}), 200

    except Exception as e:
        return jsonify({'message': 'Failed to send notification', 'error': str(e)}), 500

def send_sms(to_number, message_body):
    """
    Send SMS using Twilio API.
    """
    message = twilio_client.messages.create(
        body=message_body,
        from_=TWILIO_PHONE_NUMBER,
        to=to_number
    )
    return message.sid

def send_email(to_email, subject, message_body):
    """
    Send Email using SendGrid API.
    """
    from_email = Email("no-reply@mh-ai.com")  # Use a verified sender
    to_email = To(to_email)
    content = Content("text/plain", message_body)
    mail = Mail(from_email, to_email, subject, content)
    response = sendgrid_client.client.mail.send.post(request_body=mail.get())
    return response.status_code

if __name__ == '__main__':
    # Ensure the necessary environment variables are set
    required_env_vars = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER', 'SENDGRID_API_KEY']
    missing_env_vars = [var for var in required_env_vars if not os.environ.get(var)]
    if missing_env_vars:
        print(f"Error: Missing environment variables: {', '.join(missing_env_vars)}")
        exit(1)

    app.run(host='0.0.0.0', port=5004)

