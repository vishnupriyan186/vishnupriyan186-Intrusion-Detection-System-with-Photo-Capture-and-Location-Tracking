import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import requests
import os
from getpass import getpass


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_USER = 'vpriyan143@gmail.com'
EMAIL_PASSWORD = 'ovwwzlvqiluhpsea'
TO_EMAIL = 'vpriyan143@gmail.com'

def capture_photo(photo_path):
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    if ret:
        cv2.imwrite(photo_path, frame)
    camera.release()
def send_email(photo_path, location_link):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = 'Multiple Wrong Password Attempts Detected'

    with open(photo_path, 'rb') as file:
        mime = MIMEBase('image', 'jpeg')
        mime.set_payload(file.read())
        encoders.encode_base64(mime)
        mime.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(photo_path)}"')
        msg.attach(mime)
    
   
    body = f"Location of the attempt: {location_link}"
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)

def get_location():
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    loc = data['loc']
    latitude, longitude = loc.split(',')
    google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
    return google_maps_link

def main():
    correct_password = "securepassword"
    photo_path = 'intruder.jpg'
    attempt_count = 0
    max_attempts = 3

    while attempt_count < max_attempts:
        entered_password = getpass("Enter password: ")
        if entered_password != correct_password:
            attempt_count += 1
            print("Incorrect password!")
            if attempt_count == max_attempts:
                capture_photo(photo_path)
                location_link = get_location()
                send_email(photo_path, location_link)
        else:
            print("Welcome!")
            break

if __name__ == "__main__":
    main()