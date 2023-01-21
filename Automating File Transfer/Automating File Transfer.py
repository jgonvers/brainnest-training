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
import os, shutil, schedule, time, json, logging

TEMP_FOLDER = f"{os.getcwd()}/.temp/"
SRC_FOLDER = f"{os.getcwd()}/src/"

def download(logger,ftp,files=[],destination=None):
    for file in files:
        try:
            if file not in os.listdir(destination) and file != "frep" and file != "input":    # Only downloads files that have not been previously downloaded. The frep and input files have been excluded since they give error due to lack of permission
                logger.info(f"Downloading {file}...")
                ftp.retrbinary(f"RETR {file}",open(f"{TEMP_FOLDER}/{file}","wb").write)    # Downloads files from FTP server
                logger.info(f"Downloaded {file}.")
        except Exception as e:
            logger.exception(f"Error while trying to download {file}: {e}")

def move(logger,files=[],destination=None):
    for file in files:
        try:
            logger.info(f"Moving {file}...")
            shutil.move(f"{TEMP_FOLDER}/{file}",f"{destination}/{file}")    # Moves downloaded files from local storage to internal network folder
            logger.info(f"Moved {file}.")
        except Exception as e:
            logger.exception(f"Error moving {file}: {e}")


def main():
    logging.basicConfig(level=logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s : %(levelname)s - %(message)s")
    
    file_handler = logging.FileHandler(f"{SRC_FOLDER}/File Transfer.log")
    file_handler.setFormatter(formatter)
    
    logger = logging.getLogger("AFT")
    logger.addHandler(file_handler)

    try:
        file = open(f"{SRC_FOLDER}/settings.json")
        data = json.load(file)

        host = data["Host"]
        user = data["User"]
        password = data["Password"]
        destination = data["DownloadFolder"]
        
        logger.info("Found settings file.")
    except Exception as e:
        logger.exception(f"Could not find settings file: {e}")
        return

    if not os.path.exists(destination):
        os.makedirs(destination)

    try:
        ftp = FTP(host,user,password)    # Connects to the FTP server
    except Exception as e:
        logger.exception(f"Failed to login: {e}")
        return

    if not os.path.exists(TEMP_FOLDER):    # Creates a temporary directory to store downloaded files while not finished
        os.makedirs(TEMP_FOLDER)

    try:
        files = ftp.nlst()    # Creates a list of files available to download in the FTP server
    except Exception as e:
        logger.exception(f"Failed to retrieve list of files: {e}")
        return

    download(logger,ftp,files,destination)

    try:
        ftp.quit()
        logger.info("Successfully exited the FTP server.")
    except Exception as e:
        logger.exception("Failed to exit FTP server: {e}")
        return

    move(logger,os.listdir(TEMP_FOLDER),destination)

    try:
        os.removedirs(TEMP_FOLDER)    # Deletes temporary folder
        logger.info("Successfully removed temporary folder.")
    except Exception as e:
        logger.exception("Error deleting temporary folder: {e}")

schedule.every().day.at("20:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(1)