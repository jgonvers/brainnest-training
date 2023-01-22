import logging
from datetime import datetime as dt

from tkinter import *

from settings import log_level
from handlers import TransactionIncome, TransactionExpense, TransactionGoal

logger = logging.getLogger("GUI")
logger.setLevel(log_level)


class BudgetApp:
    def __init__(self):
        self.window = Tk()
        self.window.title("Budget App")
        self.window.geometry("500x500+150+150")
        self.income = TransactionIncome()
        self.expense = TransactionExpense()
        self.budget = TransactionGoal()

        self.button_insert = Button(
            self.window,
            text="Insert",
            width=15,
            font=(14),
            bg="green",
            fg="white",
            bd=2,
            command=self.transaction(),
        )
        self.button_insert.grid(row=1, column=1)
        self.button_set_goal = Button(
            self.window,
            text="Set goals",
            width=20,
            bg="orange",
            fg="white",
            font=(10),
            bd=2,
            command=self.goal(),
        )
        self.button_set_goal.grid(row=1, column=2)

    def transaction(self):
        new_window = Toplevel(self.window)
        new_window.title("data entry")
        new_window.geometry("400x280")

        def add_transaction(event="add_transaction"):
            transaction_data = {}
            transaction_type = entry_type.get()
            transaction_data["amount"] = entry_amount.get()
            transaction_data["description"] = entry_description.get()
            transaction_data["date"] = dt.strptime(
                entry_date.get(), "%Y-%m-%d"
            ).date()

            if transaction_type.lower() == "income":
                self.income.create(transaction_data)
            elif transaction_type.lower() == "expense":
                self.expense.create(transaction_data)

        def clear_transaction(event="clear_transaction"):
            entry_type.delete(0, END)
            entry_amount.delete(0, END)
            entry_description.delete(0, END)
            entry_date.delete(0, END)

        label_main = Label(
            new_window,
            text="Please enter data then press add",
            bg="red",
            fg="white",
            font=(4),
        )
        label_main.grid(row=1, column=1, columnspan=2)
        label_type = Label(
            new_window, text="type", width=15, bg="white", fg="black", font=(3)
        )
        label_type.grid(row=2, column=1)
        label_amount = Label(
            new_window,
            text="amount",
            width=15,
            bg="grey",
            fg="black",
            font=(3),
        )
        label_amount.grid(row=3, column=1)
        label_description = Label(
            new_window,
            text="description",
            width=15,
            bg="white",
            fg="black",
            font=(3),
        )
        label_description.grid(row=4, column=1)
        label_date = Label(
            new_window, text="date", width=15, bg="grey", fg="black", font=(3)
        )
        label_date.grid(row=5, column=1)
        entry_type = Entry(
            new_window, width=15, bg="white", fg="black", font=(3)
        )
        entry_type.grid(row=2, column=2)
        entry_amount = Entry(
            new_window, width=15, bg="grey", fg="black", font=(3)
        )
        entry_amount.grid(row=3, column=2)
        entry_description = Entry(
            new_window, width=15, bg="white", fg="black", font=(3)
        )
        entry_description.grid(row=4, column=2)
        entry_date = Entry(
            new_window, width=15, bg="grey", fg="black", font=(3)
        )
        entry_date.grid(row=5, column=2)
        button_add = Button(
            new_window,
            text="Add",
            width=10,
            font=(4),
            bg="yellow",
            fg="black",
            bd=2,
            command=add_transaction,
        )
        button_add.grid(row=6, column=1, columnspan=2)
        button_clear = Button(
            new_window,
            text="Clear",
            width=10,
            font=(4),
            bg="orange",
            fg="black",
            bd=2,
            command=clear_transaction,
        )
        button_clear.grid(row=7, column=1, columnspan=2)
        entry_type.bind("<Return>", lambda event: entry_amount.focus())
        entry_amount.bind("<Return>", lambda event: entry_description.focus())
        entry_description.bind("<Return>", lambda event: entry_date.focus())
        entry_date.bind("<Return>", lambda event: button_add.focus())
        button_add.bind("<Return>", add_transaction)

    def goal(self):
        goal_window = Toplevel(self.window)
        goal_window.title("set goals")
        goal_window.geometry("400x280")

        def add_goal(event="add_goal"):
            goal_data = {
                "amount": entry_amount.get(),
                "date": dt.strptime(entry_date.get(), "%Y-%m-%d").date(),
            }
            self.budget.create(goal_data)

        def clear_goal(event="clear_goal"):
            entry_amount.delete(0, END)
            entry_date.delete(0, END)

        label_main = Label(
            goal_window,
            text="Please enter data then press add",
            bg="red",
            fg="white",
            font=(4),
        )
        label_main.grid(row=1, column=1, columnspan=2)
        label_amount = Label(
            goal_window,
            text="amount",
            width=15,
            bg="grey",
            fg="black",
            font=(3),
        )
        label_amount.grid(row=2, column=1)
        label_date = Label(
            goal_window, text="date", width=15, bg="grey", fg="black", font=(3)
        )
        label_date.grid(row=3, column=1)
        entry_amount = Entry(
            goal_window, width=15, bg="grey", fg="black", font=(3)
        )
        entry_amount.grid(row=2, column=2)
        entry_date = Entry(
            goal_window, width=15, bg="grey", fg="black", font=(3)
        )
        entry_date.grid(row=3, column=2)
        button_add = Button(
            goal_window,
            text="Add",
            width=10,
            font=(4),
            bg="yellow",
            fg="black",
            bd=2,
            command=add_goal,
        )
        button_add.grid(row=4, column=1, columnspan=2)
        button_clear = Button(
            goal_window,
            text="Clear",
            width=10,
            font=(4),
            bg="orange",
            fg="black",
            bd=2,
            command=clear_goal,
        )
        button_clear.grid(row=5, column=1, columnspan=2)
        entry_amount.bind("<Return>", lambda event: entry_date.focus())
        entry_date.bind("<Return>", lambda event: button_add.focus())
        button_add.bind("<Return>", add_goal)

    def start(self):
        return self.window.mainloop()
