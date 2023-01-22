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

