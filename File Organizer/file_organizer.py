from pathlib import Path
import shutil
from datetime import datetime
import logging

log_level = logging.INFO
logging.basicConfig(
    encoding="utf-8",
    level=log_level,
    format="%(asctime)s %(levelname)s: %(name)s: %(message)s",
)
logger = logging.getLogger("file_organizer")

class DirOrganizer:
    def __init__(self, main_dir, mode='dry'):
        self.main_dir = main_dir
        self.type_list = []
        self.day_list = []
        self.mode = mode
        
    def files_by_type(self):
        for file in self.main_dir.iterdir():
            # print(file.name)
            if file.is_file():
                type_ext = file.suffix.removeprefix('.')
                # print(type_ext)
                if self.mode == 'dry':
                    self.show_actions(type_ext, file)
                else:
                    self.move_files(self.type_list, type_ext, file)
                
 
    def files_by_day(self):
        for file in self.main_dir.iterdir():
            print(file.name)
            date_ = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y%m%d")
            print(date_)
            if file.is_file():
                if self.mode == 'dry':
                    self.show_actions(date_, file)
                else:
                    self.move_files(self.type_list, date_, file)
  
    
    def show_actions(self, dst_dir_name, file):
        if dst_dir_name in self.type_list:
            dst_dir = self.main_dir / dst_dir_name
            logger.info(f"Would have moved '{file}' to '{dst_dir / file.name}' ")
        else:
            self.type_list.append(dst_dir_name)
            new_dir = self.main_dir / dst_dir_name
            logger.info(f"Would have moved '{file}' to '{new_dir / file.name }' ")
                
    def move_files(self, check_list, dst_dir_name, file):
        if dst_dir_name in check_list:
            dst_dir = self.main_dir / dst_dir_name
            shutil.move(file, dst_dir)
            logger.info(f"Moving '{file}' to '{dst_dir / file.name}' ")
        else:
            self.create_directory(check_list, dst_dir_name, file)   

    def create_directory(self, check_list, dst_dir_name, file):
        check_list.append(dst_dir_name)
        new_dir = self.main_dir / dst_dir_name
        Path.mkdir(new_dir)
        logger.info(f"Creating directory: '{new_dir}'")
        shutil.move(file, new_dir)
        logger.info(f"Moving '{file}' to '{new_dir }' ")   
                    


if __name__ == '__main__':
    main_dir = Path.cwd().joinpath('test', 'test01')
    
    logger.info(f"The main directory is: {main_dir}")
    d = DirOrganizer(main_dir)
    
    print("The script is running in'Dry run' mode. The program will not perform any changes.")
    
    d.files_by_type()
    d.files_by_day()
