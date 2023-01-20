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
from shutil import move
from os.path import join, exists
from os import makedirs, remove


log_file = "Automated File Transfer.log"

login = {
"host": "ftp.dlptest.com",
"user": "dlpuser",
"passwd" : "rNrKYTX9g7z3RgJRmxWuGHbeu" }  #should be taken from an external file, preferably encrypted

src_dir = ""
dest_dir = "temp"

def file_transfer(login, src_dir="", dest_dir=""):
  try:
    try:
      ftp = FTP(**login)
    except Exception as e:
      log("could not connect to {}".format(login['host']))
      log(str(e))
      return(False)
    
    if src_dir != "":
        try:
          ftp.cwd(src_dir)
        except Exception as e:
          log("could not access source folder {}".format(src_dir))
          log(str(e))
          ftp.quit()
          return(False)
    
    files = []
    try:
      ftp.retrlines('NLST', files.append)
    except Exception as e:
          log("could not list files")
          log(str(e))
          ftp.quit()
          return(False)
    
    if not exists(dest_dir):
      makedirs(dest_dir)
      
    for file in files:
        log("attempting {}".format(file))
        dest_file = join(dest_dir, file)
        if exists(dest_file):
          log("{} already exists".format(dest_file))
          continue
        with open(file, 'wb') as fp:
            try:
              ftp.retrbinary('RETR {}'.format(file), fp.write)
            except Exception as e:
              log("error downloading file")
              log(str(e))
              remove(file)
              continue
            log("downloaded")
        try:
          move(file,dest_file)
        except Exception as e:
          log("error moving file")
          log(str(e))
          remove(file)
          continue
        log("moved to {}".format(dest_file))
  except Exception as e:
    log(str(e))
    ftp.quit()
    return(False)
  ftp.quit()
  return(True)


def log(string, log_file=log_file):
  string = "{}: {}\n".format(datetime.now(), string)
  with open(log_file, 'a') as f:
    f.write(string)
  print(string)

file_transfer(login, dest_dir=dest_dir)
