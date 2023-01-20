''' You work at a company that receives daily data files from external partners. These files need to be processed and analyzed, but first, they need to be transferred to the company's internal network.

The goal of this project is to automate the process of transferring the files from an external FTP server to the company's internal network.

Here are the steps you can take to automate this process:

    Use the ftplib library to connect to the external FTP server and list the files in the directory.

    Use the os library to check for the existence of a local directory where the files will be stored.

    Use a for loop to iterate through the files on the FTP server and download them to the local directory using the ftplib.retrbinary() method.

    Use the shutil library to move the files from the local directory to the internal network.

    Use the schedule library to schedule the script to run daily at a specific time.

    You can also set up a log file to keep track of the files that have been transferred and any errors that may have occurred during the transfer process. '''

from ftplib import FTP
from datetime import datetime
import os, shutil, schedule, time

HOST = "ftp.dlptest.com"
TEMP_FOLDER = f"{os.getcwd()}/.temp/"
USER, PASSWORD = "dlpuser","rNrKYTX9g7z3RgJRmxWuGHbeu"    # Provided by the FTP server
destination = input("Insert the network location to store downloaded data:\n")    # Gets input from user to save downloaded files on desired location.

def download(ftp,log,files=[],destination=""):
    for file in files:
        try:
            if file not in os.listdir(destination):    # Only downloads files that have not been previously downloaded.
                print(f"Downloading {file}...")
                ftp.retrbinary(f"RETR {file}",open(f"{TEMP_FOLDER}/{file}","wb").write)    # Downloads files from FTP server
                log.write(f"Downloaded {file}.\n")
        except Exception as e:
            msg = f"Error while trying to download {file}"
            log.write(f"{msg} -> {e}\n")
            print(msg)

def move(log,files=[],destination=""):
    for file in files:
        try:
            print(f"Moving {file}...")
            shutil.move(f"{TEMP_FOLDER}/{file}",f"{destination}/{file}")    # Moves downloaded files from local storage to internal network folder
            log.write(f"Moved {file}.\n")
        except Exception as e:
            msg = f"Error moving {file}."
            log.write(f"{msg} -> {e}")
            print(msg)

def main():
    ftp = FTP(HOST,USER,PASSWORD)    # Connects to the FTP server
    
    log_location = f"{destination}/log.txt"

    if not os.path.exists(TEMP_FOLDER):    # Creates a temporary directory to store downloaded files while not finished
        os.makedirs(TEMP_FOLDER)

    if not os.path.exists(log_location):    # Determines if the log will be created or simply updated
        log = open(log_location,"w")
    else:
        log = open(log_location,"a")

    log.write(f"--> Start time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")    # Tracks every download instance

    files = ftp.nlst()    # Creates a list of files available to download in the FTP server
    download(ftp,log,files,destination)
    ftp.quit()

    move(log,os.listdir(TEMP_FOLDER),destination)
    log.close()
    os.removedirs(TEMP_FOLDER)    # Deletes temporary folder

schedule.every().day.at("20:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)