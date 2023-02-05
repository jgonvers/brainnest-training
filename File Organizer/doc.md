## Documentation for the Weather App

### main.py

```
def main():
    rel_main_dir = input("Please insert the path directory to organize:\n> ")
    main_dir = Path.cwd().joinpath(rel_main_dir)
```

User is asked to insert the path of the directory to organize.


```
    d = DirOrganizer(main_dir)
    
    type_or_day = input("Do you want to organize your directory by (t)ype file or modification (d)ay ?\n> ")
    print("The script is running in 'Dry run' mode. The program will not perform any changes.")
    mode = input("To deactivate 'dry run' mode please insert (y)es:\n> ")
```

An instance of class DirOrganizer is instantiated into variable 'd'.
The user is asked to choose between organization by type or by modification day.

The user is asked if he wants to change the default 'dry run' mode to 'on' mode.
The default mode is _dry run_, so the program will not perform any modification on the directory, and will only inform the user of the modifications it would have made.

```
    if mode.lower().startswith('y'):
        d.mode = 'on'
```

Deactivates _dry run_ mode.

```
    if type_or_day.startswith('d'):
        d.files_by_day()
    elif type_or_day.startswith('t'):
        d.files_by_type()
    else:
        logger.error(f"Invalid option {type_or_day}")
```

Checks what organization the user has chosen, per file type or modification day.

```
if __name__ == "__main__":
    main()
```
This code calls the main function only if this script is the main one.


### file_organizer.py

```
class DirOrganizer:
    def __init__(self, main_dir, mode='dry'):
        self.main_dir = main_dir
        self.type_list = []
        self.day_list = []
        self.mode = mode
```

Sets the directory path of the instance of class DirOrganizer. Sets default mode to _dry run_.

```
    def files_by_type(self):
        for file in self.main_dir.iterdir():
            if file.is_file():
                type_ext = file.suffix.removeprefix('.')
                if self.mode == 'dry':
                    self.show_actions(type_ext, file)
                else:
                    self.move_files(self.type_list, type_ext, file)
```

This function, `files_by_type()`, is called when the user chooses to organize by file type.

For each file, the suffix is extracted (ex.: .txt, .py, .png...) and the following directories are created (ex.: txt, py, png) and the files are moved into the respectives new directories.

```
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

```

This function, `files_by_day()`, is called when the user chooses to organize by file modification time.

A new directory is created with the date name, for instance, _20230205_ if the file was last modified on February 05 2023. The files are then moved to the respective directories.

```
    def show_actions(self, dst_dir_name, file):
        if dst_dir_name in self.type_list:
            dst_dir = self.main_dir / dst_dir_name
            logger.info(f"Would have moved '{file}' to '{dst_dir / file.name}' ")
        else:
            self.type_list.append(dst_dir_name)
            new_dir = self.main_dir / dst_dir_name
            logger.info(f"Would have moved '{file}' to '{new_dir / file.name }' ")
```

This function, `show_actions()`, is called if the user chooses to run the script in dry run mode.

It only prints the logs to the terminal of the performances it would have done.

```
    def move_files(self, check_list, dst_dir_name, file):
        if dst_dir_name in check_list:
            dst_dir = self.main_dir / dst_dir_name
            shutil.move(file, dst_dir)
            logger.info(f"Moving '{file}' to '{dst_dir / file.name}' ")
        else:
            self.create_directory(check_list, dst_dir_name, file) 
```

This function, `move_files()`, creates the new directories and moves the files to the respective new directory.

```
    def create_directory(self, check_list, dst_dir_name, file):
        check_list.append(dst_dir_name)
        new_dir = self.main_dir / dst_dir_name
        Path.mkdir(new_dir)
        logger.info(f"Creating directory: '{new_dir}'")
        shutil.move(file, new_dir)
        logger.info(f"Moving '{file}' to '{new_dir }' ")  
```

This function, `create_directory()`, is called by the previous one. It is used when the directory has not been created yet. It creates the new directory and moves the respective file into it.

### settings.py

```
log_level = logging.INFO
logging.basicConfig(
    encoding="utf-8",
    level=log_level,
    format="%(asctime)s %(levelname)s: %(name)s: %(message)s",
)
logging.getLogger("settings").setLevel(log_level)
```
Set up the logging