import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.utils
from datetime import datetime
import requests
from os import environ
from base64 import b64decode

# Streaming
streaming_host = environ.get("STREAMING_HOST")
streaming_port = environ.get("STREAMING_PORT")

# Email configuration
smtp_server = environ.get("SMTP_SERVER")
smtp_port = environ.get("SMTP_PORT")
smtp_username = environ.get("SMTP_USERNAME")
smtp_password = b64decode(environ.get("SMTP_PASSWORD")).decode('utf-8')

recipient_email = environ.get("RECIPIENT_EMAIL")
subject = f"Stream {streaming_host}:{streaming_port} is down"
message = subject

def check_stream_status(host: str, port: int) -> str:
    """Check whether the stream on the given Icecast host and port is up or down.

    Args:
        host (str): The Icecast host.
        port (int): The Icecast port.

    Returns:
        str: "Stream is up" if the stream is running, "Stream is down" otherwise.
    """
    # Define the URL for the status JSON endpoint
    status_url = f"http://{host}:{port}/status-json.xsl"

    # Fetch the status data from the Icecast server
    response = requests.get(status_url)

    # Check if the data was fetched successfully
    if response.status_code == 200:
        # Parse the JSON data
        status_dat = response.json()

        # Check if the 'source' key exists within the 'icestats' dictionary
        icestats = status_dat.get('icestats')
        source = icestats.get('source') if icestats else None

        # Return the appropriate message based on the presence of the 'source' key
        if source:
            print('Stream is Up')
            return

    print('Stream is Down')
    send_email()

def send_email():
    """Send an email notification."""

    # Decode the base64-encoded password

    sender_email = smtp_username
    
    # Create a MIMEText object to represent the email message
    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = recipient_email
    email_message['Subject'] = subject
    email_message['Date'] = email.utils.formatdate(localtime=True)

    # Attach the text message
    email_message.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, email_message.as_string())

    print('Email sent successfully')

check_stream_status(streaming_host, streaming_port)
