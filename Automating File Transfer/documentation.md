# Automatic File Transfer
## Imports
```
import os
import json
import time
import shutil
import logging
import schedule
from ftplib import FTP
```
> Libraries used in the code.
***
## Global
```
DAILY_TIME = "20:00"
```
> This global constant is used to set the time the transfer will occur.
```
SRC_FOLDER = os.path.join(os.getcwd(), "src")
TEMP_FOLDER = os.path.join(os.getcwd(), ".temp")
```
> The SRC_FOLDER and TEMP_FOLDER are global constants that store the paths to folders used in the project
```
FORMAT = "%(asctime)s : %(levelname)s - %(message)s"
```
> The FORMAT global constant stores the format that is used by the logger.
***
## Logger Configuration
```
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
```
> This code uses the basicConfig fuction in the logging library to make messages with DEBUG level or higher appear in the log. It also sets the format the logger will use.
```
file_handler = logging.FileHandler(os.path.join(SRC_FOLDER,
                                                "File Transfer.log"))
file_handler.setFormatter(logging.Formatter(FORMAT))
```
> This code sets a FileHandler to store the log events in a file.
```
logger = logging.getLogger("AFT")
logger.addHandler(file_handler)
```
> This code creates the logger, gives it the name "AFT" and associates the file_handler to it.
***
## Main function
```
def main():
    try:
        with open(os.path.join(SRC_FOLDER, "settings.json"), "r") as file:
            data = json.load(file)

            host = data["Host"]
            user = data["User"]
            password = data["Password"]
            destination = data["DownloadFolder"]

        logger.info("Found settings file.")
    except Exception as e:
        logger.exception(f"Could not find settings file: {e}")
        return

    # Creates destination folder
    if not os.path.exists(destination):
        os.makedirs(destination)

    try:
        # Establishes connection to FTP server
        ftp = FTP(host, user, password)
        logger.info("Successfully connected to the FTP server.")
    except Exception as e:
        logger.exception(f"Failed to login: {e}")
        return

    # Creates temporary folder
    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)

    try:
        # Get the list of all files available to download in FTP server
        files = ftp.nlst()
    except Exception as e:
        logger.exception(f"Failed to retrieve list of files: {e}")
        return

    download(ftp, files, os.listdir(destination))

    try:
        ftp.quit()
        logger.info("Successfully exited the FTP server.")
    except Exception as e:
        logger.exception("Failed to exit FTP server: {e}")
        return

    move(destination, os.listdir(TEMP_FOLDER))

    try:
        # Deletes temporary folder
        os.removedirs(TEMP_FOLDER)
        logger.info("Successfully removed temporary folder.")
    except Exception as e:
        logger.exception("Error deleting temporary folder: {e}")
```
### Main function breakdown
```
try:
    with open(os.path.join(SRC_FOLDER, "settings.json"), "r") as file:
        data = json.load(file)
```
>Loads the JSON file that is located in the SRC_FOLDER.
```
host = data["Host"]
user = data["User"]
password = data["Password"]
destination = data["DownloadFolder"]
```
>Stores the data received from the JSON file in variables. 
```
logger.info("Found settings file.")
```
> Puts in the log that the program was successful in retrieving the needed information.
```
except Exception as e:
    logger.exception(f"Could not find settings file: {e}")
    return
```
> If an error occur while trying to get the data in the JSON file, the error will be stored in the log file and the code execution will be stopped.
```
if not os.path.exists(destination):
    os.makedirs(destination)
```
> Verifies if the destination path exists and, if it doesn't, creates the folder.
```
try:
    ftp = FTP(host, user, password)
    logger.info("Successfully connected to the FTP server.")
```
> Tries to establish a connection to the FTP server. If successful, inform it to the log.
```
except Exception as e:
    logger.exception(f"Failed to login: {e}")
    return
```
> If there was an error while connecting to the FTP server, the error will be stored in the log file and the code execution will stop.
```
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)
```
> Verifies if the temporary download folder exists and, if it doesn't, creates it.
```
try:
    files = ftp.nlst()
```
> Tries to get a list of all the files that are available in the FTP server.
```
except Exception as e:
    logger.exception(f"Failed to retrieve list of files: {e}")
    return
```
> If there was an error during the retrieval of the list of files, the error will be stored in the log and the code execution will stop.
```
download(ftp, files, os.listdir(destination))
```
> Calls the Download function.
```
try:
    ftp.quit()
    logger.info("Successfully exited the FTP server.")
```
> Tries to end the connection to the FTP server and, if successful, inform the log.
```
except Exception as e:
    logger.exception("Failed to exit FTP server: {e}")
    return
```
> If there was an error while ending the connection to the FTP server, stores the error in the log and stops the code execution.
```
move(destination, os.listdir(TEMP_FOLDER))
```
> Calls the move function.
```
try:
    os.removedirs(TEMP_FOLDER)
    logger.info("Successfully removed temporary folder.")
```
> Tries to delete the temporary download folder and, if successful, informs the log.
```
except Exception as e:
    logger.exception("Error deleting temporary folder: {e}")
```
> If there was an error while trying to delete the temporary download folder, stores the error in the log.
***
## Download function
```
def download(ftp, files=[], downloaded_files=[]):
    for file in files:
        try:
            if file not in downloaded_files and file not in ("frep", "input"):
                logger.info(f"Downloading {file}...")
                file_path = os.path.join(TEMP_FOLDER, file)
                ftp.retrbinary(f"RETR {file}", open(file_path, "wb").write)
                logger.info(f"Downloaded {file}.")

        except Exception as e:
            logger.exception(f"Error while trying to download {file}: {e}")
```
>The function receives the FTP server created in the main function (ftp), the names of the files that need to be downloaded (files) and a list of the files that have been previously downloaded (downloaded_files).
***
### Download function breakdown
```
for file in files:
```
> Will try to download every file available.
```
try:
    if file not in downloaded_files and file not in ("frep", "input"):
```
> These conditions were put in place so that the code doesn't download the same files more than once and to stop it from trying to download the files "frep" and "input". This was put in place because these files threw an error due to lack of permissions.
```
logger.info(f"Downloading {file}...")
```
> Puts in the log the attempt to download a given file.
```
file_path = os.path.join(TEMP_FOLDER, file)
```
> Gets the path to the temporary folder where the files will be stored.
```
ftp.retrbinary(f"RETR {file}", open(file_path, "wb").write)
```
> Downloads a given file into the temporary folder.
```
logger.info(f"Downloaded {file}.")
```
> Puts in the log that the download was successful.
```
except Exception as e:
    logger.exception(f"Error while trying to download {file}: {e}")
```
> Puts in the log that an error occurred while trying to download a given file. The log will have the details of the error.
***
## Move function
```
def move(destination, files=[]):
    for file in files:
        try:
            logger.info(f"Moving {file}...")
            # Moves the files
            shutil.move(os.path.join(TEMP_FOLDER, file),
                        os.path.join(destination, file))
            logger.info(f"Moved {file}.")
        except Exception as e:
            logger.exception(f"Error moving {file}: {e}")
```
> This function receives the path to where the files should be moved (destination) and a list of file names (files). It then moves all the files from the temporary folder to the folder that was designated in settings.json.
***
### Move function breakdown
```
for file in files:
```
>Will try to move every file that was requested.
```
try:
    logger.info(f"Moving {file}...")
```
>Puts in the log that an attempt was made to move the given file.
```
shutil.move(os.path.join(TEMP_FOLDER, file), os.path.join(destination, file))
```
>Tries to move the file in TEMP_FOLDER to the destination folder.
```
logger.info(f"Moved {file}.")
```
>Puts in the log that the file transfer was successful.
```
except Exception as e:
            logger.exception(f"Error moving {file}: {e}")
```
>Puts in the log that an error occurred while trying to move the file. The log will have the details of the error.
***
## Scheduler
```
schedule.every().day.at(DAILY_TIME).do(main)
```
> Specifies the time the program should run the main function.
```
while True:
    schedule.run_pending()
    time.sleep(1)
```
>Loop to check the schedule and run the task at the specified time.