import socket
import threading
import smtplib

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = ''
SENDER_PASSWORD = ''
RECIPIENT_EMAIL = 'syedahmedalis14@gmail.com'

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))


def send_email(subject, content):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            email_subject = f"Subject: {subject}"
            email_content = f"{email_subject}\n\n{content}"
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, email_content)
            print("Email notification sent.")
    except smtplib.SMTPException as e:
        print("An error occurred while sending the email:", e)
def chat():
    while True:
        message = input("")
        if message == 'email':
            subject = input("Enter the email subject: ")
            content = input("Enter the email content: ")
            send_email(subject, content)
        else:
            send_chat_message(message)

def send_chat_message(message):
    message = f'{nickname}: {message}'
    client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

chat()