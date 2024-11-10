from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import logging

def send_order_confirmation_email(target_email: str, order_value: float) -> bool:
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.seznam.cz")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

    # Create message
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = target_email
    msg['Subject'] = "Your 3D Printing Quote"

    # Email body
    body = f"""Hello!

We now know about your quote of approximate value €{order_value:.2f}!

Reply to this email or contact me on discord, so we can arrange the printing.

Join the discord server: https://discord.gg/apyDuC2MaM

Best regards,
PrintLab


If you received this email by mistake, please reply to this email and let us know.
"""

    msg.attach(MIMEText(body, 'plain'))

    try:
        logging.info(f"Sending email to {target_email}")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        logging.info(f"Connected to SMTP server")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        logging.info(f"Logged in")

        server.send_message(msg)
        logging.info(f"Email sent")
        server.quit()
        return True

    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        return False
