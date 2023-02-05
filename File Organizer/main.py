from pathlib import Path
from settings import log_level
from file_organizer import DirOrganizer
import logging

logger = logging.getLogger("main")
logger.setLevel(log_level)


if __name__ == '__main__':
    rel_main_dir = input("Please insert the path directory to organize:\n> ")
    main_dir = Path.cwd().joinpath(rel_main_dir)
    
    logger.debug(f"The main directory is: {main_dir}")
    d = DirOrganizer(main_dir)
    type_or_day = input("Do you want to organize your directory by (t)ype file or modification (d)ay ?\n> ")
    print("The script is running in'Dry run' mode. The program will not perform any changes.")
    mode = input("To deactive 'dry run' mode please insert (y)es:\n> ")
    
    if mode.lower().startswith('y'):
        d.mode = 'on'
    
    if type_or_day.startswith('d'):
        d.files_by_day()
    elif type_or_day.startswith('t'):
        d.files_by_type()
    else:
        logger.error(f"Invalid option {type_or_day}")