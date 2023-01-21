''' You work at a company that sends daily reports to clients via email. The goal of this project is to automate the process of sending these reports via email.

Here are the steps you can take to automate this process:

    Use the smtplib library to connect to the email server and send the emails.

    Use the email library to compose the email, including the recipient's email address, the subject, and the body of the email.

    Use the os library to access the report files that need to be sent.

    Use a for loop to iterate through the list of recipients and send the email and attachment.

    Use the schedule library to schedule the script to run daily at a specific time.

    You can also set up a log file to keep track of the emails that have been sent and any errors that may have occurred during the email sending process. '''

# TODO: Set up log file to keep track of any events that happened during code execution
# TODO: Handle exceptions

from smtplib import SMTP
import os, schedule, time
from datetime import datetime
from email.message import EmailMessage

EMAIL_LIST = []
ATTACHMENT_DIRECTORY = f"{os.getcwd()}/Reports"    # Created a directory with multiple report files to attach to email

def generate_email(sender="",subject="",receiver="",time_stamp=""):
    e = EmailMessage()
    e["To"] = receiver
    e["From"] = "Brainnest - Automatic Email Sending"
    e["Subject"] = subject
    e.set_content(f"""
    This is an automatic email sent @ {time_stamp}.

    This email was sent from {sender} to {receiver}

    This email will be sent every 24 hours.
    """)
    for file in os.listdir(ATTACHMENT_DIRECTORY):    # Attaches all files
        try:
            f = open(f"{ATTACHMENT_DIRECTORY}/{file}","rb")
            e.add_attachment(f.read(),maintype='application',subtype="txt",filename=file)
        except Exception as e:
            print(e)

    return e.as_string()

def send(smtp,sender_mail="",mail_obj="",receiver_mail=""):
    try:
        smtp.sendmail(sender_mail,receiver_mail,mail_obj)
    except Exception as e:
        print(e)

def main():
    smtp = SMTP("smtp.gmail.com",587)
    smtp.starttls()
    
    sender_mail = input("Enter your email:\n")
    password = input("Enter your password:\n")

    smtp.login(sender_mail,password)

    for receiver_mail in EMAIL_LIST:
        time_stamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        subject = "Automatic mail."
        mail_obj = generate_email(sender_mail,subject,receiver_mail,time_stamp)
        send(smtp,sender_mail,mail_obj,receiver_mail)

schedule.every().day.at("20:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)