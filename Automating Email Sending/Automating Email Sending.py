''' You work at a company that sends daily reports to clients via email. The goal of this project is to automate the process of sending these reports via email.

Here are the steps you can take to automate this process:

    Use the smtplib library to connect to the email server and send the emails.

    Use the email library to compose the email, including the recipient's email address, the subject, and the body of the email.

    Use the os library to access the report files that need to be sent.

    Use a for loop to iterate through the list of recipients and send the email and attachment.

    Use the schedule library to schedule the script to run daily at a specific time.

    You can also set up a log file to keep track of the emails that have been sent and any errors that may have occurred during the email sending process. '''


from smtplib import SMTP
import os, schedule, time, logging
from datetime import datetime
from email.message import EmailMessage

ATTACHMENT_DIRECTORY = f"{os.getcwd()}/Reports"    # Created a directory with multiple report files to attach to email

def generate_email(sender=None,subject=None,receiver=None,time_stamp=None,logger=None):
    e = EmailMessage()
    e["To"] = receiver
    e["From"] = "Brainnest - Automatic Email Sending"
    e["Subject"] = subject
    e.set_content(f"""
    This is an automatic email sent @ {time_stamp}.

    This email was sent from {sender} to {receiver}

    This email will be sent every 24 hours.
    """)

    logger.debug(f"Reports are in directory: {ATTACHMENT_DIRECTORY}")
    for file in os.listdir(ATTACHMENT_DIRECTORY):    # Attaches all files
        try:
            with open(f"{ATTACHMENT_DIRECTORY}/{file}","rb") as f:
                e.add_attachment(f.read(),maintype='application',subtype="txt",filename=file)
                logger.info(f"Report {file} has been attached to the email.")
        except:
            logger.exception(f"Report {file} was not attached to the email.")

    return e.as_string()

def send(smtp, sender_mail=None, mail_obj=None, receiver_mail=None, logger=None):
    try:
        smtp.sendmail(sender_mail, receiver_mail, mail_obj)
        logger.info(f"Email from {sender_mail} has been sent to {receiver_mail}")
    except:
        logger.exception(f"Email from {sender_mail} was not sent to {receiver_mail}.")

def main():

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s %(message)s")
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('send_email.log')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    smtp = SMTP("smtp.gmail.com",587)
    smtp.starttls()
    
    cwd = os.getcwd()

    with open(f"{cwd}/sender_email.txt","r") as rf1, open(f"{cwd}/sender_email_pwd.txt","r") as rf2:
        try:
            sender_mail = rf1.readline()
            logger.debug(f"The sender email is: {sender_mail}")
        except:
            logger.exception("Could NOT read the file with the email. Ending program.")
            return 1
        
        try:
            password = rf2.readline()
            logger.debug("Password has been read.")
        except:
            logger.exception("Could NOT read the email password. Ending program.")
            return 2

    try:
        smtp.login(sender_mail, password)
        logger.debug("successful logged in.")
    except:
        logger.exception(f"Could NOT login to email {sender_mail}. Ending program")


    try:
        EMAIL_LIST = []
        with open(f"{cwd}/receivers_email.txt","r") as rf:
            lines = rf.readlines()
            for line in lines:
                line = line.strip()
                EMAIL_LIST.append(line)
    except:
        logger.exception("The list of receivers was NOT found. Ending Program")
        return 3

    logger.debug(f"The list of receivers is: {EMAIL_LIST}")
    
    for receiver_mail in EMAIL_LIST:
        time_stamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        logger.debug(f"Time stamp is: {time_stamp}")
        subject = "Automatic mail."
        mail_obj = generate_email(sender_mail,subject,receiver_mail,time_stamp, logger)
        send(smtp,sender_mail,mail_obj,receiver_mail, logger)

schedule.every().day.at("15:32").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)