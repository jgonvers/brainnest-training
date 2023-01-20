''' You work at a company that sends daily reports to clients via email. The goal of this project is to automate the process of sending these reports via email.

Here are the steps you can take to automate this process:

    Use the smtplib library to connect to the email server and send the emails.

    Use the email library to compose the email, including the recipient's email address, the subject, and the body of the email.

    Use the os library to access the report files that need to be sent.

    Use a for loop to iterate through the list of recipients and send the email and attachment.

    Use the schedule library to schedule the script to run daily at a specific time.

    You can also set up a log file to keep track of the emails that have been sent and any errors that may have occurred during the email sending process. '''

import smtplib
from email.message import EmailMessage
import logging
import os
import schedule
import time


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s %(message)s")

logger = logging.getLogger(__name__)

handler = logging.FileHandler('test.log')
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

# Input the email adress for the sender
company_email = input("Input sender gmail address: \n")

# Input the app password for the email
company_passwd = input("Please enter your password: \n")

# Below are 2 temporary emails, please create yours and edit the adrress list
client_email_list = ["hecaroc690@moneyzon.com","sevod30840@minterp.com"]

subject = "Daily Report auto"
message = """
Dear All,

The report for today is attached on this email.
"""

# Previously created a directory called `reports` on my cwd with a .txt file in it.
report_filename = os.listdir('reports')[0]
report_filename_full_path = os.path.join(os.getcwd(),'reports',report_filename)

logger.info(f"File to attach: {report_filename_full_path}")

server = smtplib.SMTP('smtp.gmail.com', 587)
# server.set_debuglevel(2)
server.starttls()
server.login(company_email, company_passwd)

def auto_email(server, client_email_list, company_email, subject, message, report_filename_full_path, report_filename):
    for client_email in client_email_list:
        em = EmailMessage()
        em['From'] = company_email
        em['subject'] = subject
        em.set_content(message)
        em['To'] = client_email
        with open(report_filename_full_path, 'rb') as rf:
            content = rf.read()
            em.add_attachment(content, maintype='application', subtype='txt', filename=report_filename)
        try:
            server.sendmail(company_email, client_email, em.as_string())
            logger.info(f"Email has been sent to {client_email}")
        except:
            logger.exception("Email was not sent.")

schedule.every().day.at("21:05").do(auto_email, server, client_email_list, company_email, subject, message, report_filename_full_path, report_filename)

while True:
    schedule.run_pending()
    time.sleep(1)
