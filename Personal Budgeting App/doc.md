## Documentation for Personal Budgeting App

### main.py
```
def main():
    while True:
        try:
            app = BudgetApp()
            app.start()
```
This code creates an instance of the `BudgetApp` class and starts the application.
```
except Exception as e:
    logger.error(e)
    continue
```
This code catches all the exceptions and logs them. It is used to prevent the application from crashing.
```
if __name__ == "__main__":
    main()
```
This code starts the application.

### Database.py
```
engine = create_engine(db_settings.db_url, echo=db_echo)
Base = declarative_base()
session = Session(engine)
```
This is the database connection code. It creates a database engine, a base class for the database, and a session for the database.

```
class Transaction(Base):
```
This class used as an abstract class for Income and Expense tables.
Transaction class has method `to_dict` which returns a dictionary of the object, used for report and plot

```
class TransactionType(Base):
```
Class used to define the type of transaction. It has a one to many relationship with Transaction class.
This table is filled automatically when connection to database created.

```
class Income(Transaction):
class Expense(Transaction):
```
This classes is for `Income` and `Expense` tables. They are inherited from Transaction class.
```
class Goal(Base):
```
Class to set budget goal.
```
Base.metadata.create_all(engine)
```
This line creates all tables in the database.
```
types = [TransactionType(name="Income"), TransactionType(name="Expense")]
try:
    insert_types = session.bulk_save_objects(types)
    session.commit()
except IntegrityError:
    session.rollback()
except AttributeError:
    session.rollback()
```
this lines creates `Income` and `Expense` types in the database.
if this types is already exist in the database, it will catch an error and rollback the session.

### GUI.py
```
class BudgetApp:
```
This class is the main class of the application. It has all the methods to create the GUI and connect it to the database.
```
def __init__(self):
```
This method creates the main window of the application,
also it initialize the db connection and creates variables for `income`, `expense` and `goal` tables.
```
def transaction(self):
```
This function creates a transaction window. It has four fields (`type`, `amount`, `description` and `date`) to create a transaction.
```
def add_transaction():
```
This function adds a transaction to the database. It gets the values from the transaction window and creates a new transaction dictionary, which is passed to income or expense create method.
```
if transaction_type.lower() == "income":
    self.income.create(transaction_data)
elif transaction_type.lower() == "expense":
    self.expense.create(transaction_data)
```
Checks the type of transaction and calls the create method of the appropriate table.
```
def clear_transaction():
```
This function clears the transaction window.
```
label_main = TKUtils.create_label(
    new_window, "Please enter data then press add", width=30
)
label_main.grid(row=1, column=1, columnspan=2)

label_type = TKUtils.create_label(new_window, "type", width=10)
label_type.grid(row=2, column=1) .......
```
This code creates the labels and entry fields for the transaction window.
```
def transaction_goal(self):
```
This function creates a goal window. It has two fields (`amount` and `date`) to create a goal.
```
def add_goal():
```
This function adds a goal to the database. It gets the values from the goal window and creates a new goal dictionary, which is passed to goal create method.
```
def clear_goal():
```
This function clears the goal window.
```
def generate_plot(self) -> str:
```
This function generates a plot of the transactions data. It uses `matplotlib` library to create a plot.
```
def generate_report(self) -> str:
```
This function generates a report of the transactions data. It uses `pandas` library to create a report.
```
def start(self):
```
This function starts the application. It creates the main window and starts the main loop.

### handlers.py
```
class DBTransaction:
```
This class is the abstract class for `Income` and `Expense` classes. It has methods to create, read, update and delete transactions.
```
class TransactionIncome(DBTransaction):
class TransactionExpense(DBTransaction):
class TransactionGoal(DBTransaction):
```
These classes are inherited from `DBTransaction` class. They have methods to create, read, update and delete transactions.
```
def fill_db(n=10000):
```
This function fills the database with random transactions. It is used for testing purposes.
```
if __name__ == "__main__":
    """Test"""
    fill_db()
    exit()
```
This code is used to fill the database with random transactions. It is used for testing purposes.

### settings.py
```
load_dotenv()
```
This line loads the environment variables from the `development.env` file.
```
class BaseSettings(pydantic.BaseSettings):
```
This class is the base class for all settings classes. It has the `env_file` variable, which is used to load the environment variables from the `development.env` file.
```
class DBSettings(BaseSettings):
```
This class is used to get the database settings from the environment variables.
```
log_level = logging.INFO
logging.basicConfig(
    filename="budget.log",
    encoding="utf-8",
    level=log_level,
    format="%(asctime)s %(levelname)s: %(name)s: %(message)s",
)
logging.getLogger("sqlalchemy").setLevel(log_level)
db_echo = log_level == logging.DEBUG
```
set up the logging
```
db_settings = SQLiteSettings()
```
This line creates an instance of the `DBSettings` class.

### utils.py
```
class TKUtils:
```
This class is used to create tkinter widgets. It has methods to create labels, entry fields and buttons. 
It is used to reduce the code duplication.
```
def create_label(
    master: tk.Tk, text: str, width: int = 10, height: int = 1
) -> tk.Label:
```
This function creates a label.
```
def create_entry(
    master: tk.Tk, width: int = 10, height: int = 1
) -> tk.Entry:
```
This function creates an entry field.
```
def create_button(
    master: tk.Tk,
    text: str,
    width: int = 10,
    height: int = 1,
    command: Callable = None,
) -> tk.Button:
```
This function creates a button.

## plot.py

`import pandas as pd`  
`import numpy as np`  
`import logging`  
`from datetime import datetime as date`  
`from tempfile import gettempdir`  
`from os.path import join, exists`  
`import matplotlib.pyplot as plt`  
`from random import randrange`  
`from os import makedirs`  

import external things used in this file  
`randrange` `makedirs` `exists` `gettempdir` where used to generate a temporary folder to hold the image generated, somehow tkinter didn't work with it

`from settings import log_level`  
`from handlers import TransactionIncome, TransactionExpense, TransactionGoal`  

import of things used from this project

`logger = logging.getLogger("plot")`  
`logger.setLevel(log_level)` 

setup the logger for this file, which allow with the format set in settings to see where the logs come from the log level is harmonised from settings

`class Plotter:`  

creation of a class for the generation of the plot and the data for the table

&nbsp;&nbsp;&nbsp;&nbsp;`def __init__(self):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.income = TransactionIncome()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.expense = TransactionExpense()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.goal = TransactionGoal()`  

add the connection to the db

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# self.temp_dir = join(gettempdir(), "budgetingapp")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# if not exists(self.temp_dir):`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`#     makedirs(self.temp_dir)`  

was used to create the temp folder for the image

&nbsp;&nbsp;&nbsp;&nbsp;`def generate_bar_plot(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self, size_x=500, size_y=500, by="day", window=None, width=10`  
&nbsp;&nbsp;&nbsp;&nbsp;`):`  

function for generating the bar plot, return the path to the image, window is a stub to allow to more easily add the feature to generate partial graph (from x to y) instead of alway all the data

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`dpi = 100`  

set the dpi of the image, magic number

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`figsize = (size_x / dpi, size_y / dpi)`  

create a tuple for the figure size, in inch

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# modify if adding an windows (from x to y )`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if window is None or True:`  

continuation of the stub for the windowing of the data, will alway return true

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`income = list(map(lambda x: x.to_dict(), self.income.get_all()))`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`expense = list(map(lambda x: x.to_dict(), self.expense.get_all()))`  

get all the data, the get all return a list of model, so a map is used to transfrom it in a list of dict

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`else:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`pass  # use a getter for the window` 

the logic for partial data should go there 
and you would neet to remove the preceding `or True`to actually get here

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`income = self._sum_by(income, by)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`in_x = [x[0] for x in income]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`in_y = [x[1] for x in income]`  

sum the income after grouping by day|month|year, then split the data in 2 list for the plot

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`expense = self._sum_by(expense, by)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`expense = [(x[0], -x[1]) for x in expense]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ex_x = [x[0] for x in expense]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ex_y = [x[1] for x in expense]`  

same thing for expense but also switch the value of the amount

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`fig, ax = plt.subplots()`  

create the plot

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`fig.set_size_inches(*figsize)`  

set the size

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`fig.set_dpi(dpi)`  

set the dpi

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`rects1 = ax.bar(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`in_x,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`in_y,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`label="Income",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`color="green",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`width=width,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`align="edge",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`  

add the data for the income

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`rects2 = ax.bar(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ex_x,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ex_y,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`label="Expense",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`color="red",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`width=-width,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`align="edge",`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`  

add the data for the expense
the side of the bars are aligned with the ticks, and the positivity of the width give the side of the ticks

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ax.set_ylabel("Amount")`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ax.set_xlabel("Date")`  

label for the axis

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ax.legend()`  

show legend

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ax.xaxis_date()`  

tell the plot to take the x axis as date

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# location = join(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`#     self.temp_dir, "figure{}.png".format(randrange(int(1e20)))`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`# )`  

used for creating temp file in the temp folder

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`location = "figure.png"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`plt.savefig(location)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return location`  

save the image to an hardcoded location and return it

&nbsp;&nbsp;&nbsp;&nbsp;`def generate_frame(self):`

generate an panda frame of all the data

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return self._create_frame(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`map(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`lambda x: x.to_dict(),`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`self.expense.get_all() + self.income.get_all(),`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`  

generate a map of all data for to_dict it

&nbsp;&nbsp;&nbsp;&nbsp;`@staticmethod`  
&nbsp;&nbsp;&nbsp;&nbsp;`def _create_frame(transactions_list):`  

create a panda frame from a list|map (probably also other iterable) of dict

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return pd.DataFrame.from_dict(transactions_list)`  

just call the tool to generate the fram from dict

&nbsp;&nbsp;&nbsp;&nbsp;`@staticmethod`  
&nbsp;&nbsp;&nbsp;&nbsp;`def _sum_by(dict_list, by="day"):`  

sum by grouping (day|month|year)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if by == "month":`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`format = "%Y-%m"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`elif by == "year":`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`format = "%Y"`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`else:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`format = "%Y-%m-%d"`  

depending of which grouping use a different format for the date the date will do date->string->date

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`grouped = {}`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`for tr in dict_list:`  

iterate over the whole list, create a key for each group and sum the content

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`key = tr["date"].strftime(format)`  

generate the key from the date and the format used

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if key in grouped:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`grouped[key] += tr["amount"]`  

if already in the dict add to it

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`else:`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`grouped[key] = tr["amount"]`  

create the key if needed, could have used a defaultdict to bypass the need for the condition

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`return [`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`(`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`date.strptime(key, format),`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`value,`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`for (key, value) in grouped.items()`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`]`  

generate the list of tuple of (date, value), using format to convert back to a date instead of a string

`if __name__ == "__main__":`  
&nbsp;&nbsp;&nbsp;&nbsp;`pl = Plotter()`  
&nbsp;&nbsp;&nbsp;&nbsp;`print(pl.generate_bar_plot(1000, 800, by="day", width=10))`  
&nbsp;&nbsp;&nbsp;&nbsp;`print(pl.generate_frame())`  

used to test during development
