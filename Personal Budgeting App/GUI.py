import logging
from datetime import datetime as dt
import tkinter as tk
from PIL import ImageTk, Image

from settings import log_level
from handlers import TransactionIncome, TransactionExpense, TransactionGoal
from plot import Plotter
from utils import TKUtils

logger = logging.getLogger("GUI")
logger.setLevel(log_level)


class BudgetApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Budget App")
        self.window.geometry("500x500+150+150")
        self.income = TransactionIncome()
        self.expense = TransactionExpense()
        self.goal = TransactionGoal()
        self.plotter = Plotter()

        self.button_insert = TKUtils.create_button(
            self.window, "Insert", self.transaction
        )
        self.button_insert.grid(row=1, column=1)

        self.button_set_goal = TKUtils.create_button(
            self.window, "Set goals", self.transaction_goal
        )
        self.button_set_goal.grid(row=1, column=2)

        self.button_plot = TKUtils.create_button(
            self.window, "Plot", self.generate_plot
        )
        self.button_plot.grid(row=2, column=1)

        self.button_report = TKUtils.create_button(
            self.window, "Report", self.generate_report
        )
        self.button_report.grid(row=2, column=2)

    def transaction(self):
        new_window = tk.Toplevel(self.window)
        new_window.title("data entry")
        new_window.geometry("400x280")

        def add_transaction():
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

        def clear_transaction():
            entry_type.delete(0, tk.END)
            entry_amount.delete(0, tk.END)
            entry_description.delete(0, tk.END)
            entry_date.delete(0, tk.END)

        label_main = TKUtils.create_label(
            new_window, "Please enter data then press add", width=30
        )
        label_main.grid(row=1, column=1, columnspan=2)

        label_type = TKUtils.create_label(new_window, "type", width=10)
        label_type.grid(row=2, column=1)

        label_amount = TKUtils.create_label(new_window, "amount", width=10)
        label_amount.grid(row=3, column=1)

        label_description = TKUtils.create_label(
            new_window, "description", width=10
        )
        label_description.grid(row=4, column=1)

        label_date = TKUtils.create_label(new_window, "date", width=10)
        label_date.grid(row=5, column=1)

        entry_type = TKUtils.create_entry(new_window)
        entry_type.grid(row=2, column=2)

        entry_amount = TKUtils.create_entry(new_window)
        entry_amount.grid(row=3, column=2)

        entry_description = TKUtils.create_entry(new_window)
        entry_description.grid(row=4, column=2)

        entry_date = TKUtils.create_entry(new_window)
        entry_date.grid(row=5, column=2)

        button_add = TKUtils.create_button(new_window, "Add", add_transaction)
        button_add.grid(row=6, column=1, columnspan=2)

        button_clear = TKUtils.create_button(
            new_window, "Clear", clear_transaction
        )
        button_clear.grid(row=7, column=1, columnspan=2)

        entry_type.bind("<Return>", lambda event: entry_amount.focus())
        entry_amount.bind("<Return>", lambda event: entry_description.focus())
        entry_description.bind("<Return>", lambda event: entry_date.focus())
        entry_date.bind("<Return>", lambda event: button_add.focus())
        button_add.bind("<Return>", add_transaction)

    def transaction_goal(self):
        goal_window = tk.Toplevel(self.window)
        goal_window.title("set goals")
        goal_window.geometry("400x280")

        def add_goal():
            goal_data = {
                "amount": entry_amount.get(),
                "date": dt.strptime(entry_date.get(), "%Y-%m-%d").date(),
            }
            self.goal.create(goal_data)

        def clear_goal():
            entry_amount.delete(0, tk.END)
            entry_date.delete(0, tk.END)

        label_main = TKUtils.create_label(
            goal_window, "Please enter data then press add"
        )
        label_main.grid(row=1, column=1, columnspan=2)

        label_amount = TKUtils.create_label(goal_window, "amount", width=10)
        label_amount.grid(row=2, column=1)

        label_date = TKUtils.create_label(goal_window, "date", width=10)
        label_date.grid(row=3, column=1)

        entry_amount = TKUtils.create_entry(goal_window)
        entry_amount.grid(row=2, column=2)

        entry_date = TKUtils.create_entry(goal_window)
        entry_date.grid(row=3, column=2)

        button_add = tk.Button(goal_window, text="Add", command=add_goal)
        button_add.grid(row=4, column=1, columnspan=2)
        button_clear = tk.Button(goal_window, text="Clear", command=clear_goal)
        button_clear.grid(row=5, column=1, columnspan=2)
        entry_amount.bind("<Return>", lambda event: entry_date.focus())
        entry_date.bind("<Return>", lambda event: button_add.focus())
        button_add.bind("<Return>", add_goal)

    def generate_plot(self) -> str:
        file_path = self.plotter.generate_bar_plot(
            1000, 800, by="month", width=10
        )
        new_window = tk.Toplevel()
        label = tk.Label(new_window, text="Plot")
        label.pack()
        img = ImageTk.PhotoImage(Image.open(file_path))
        img_label = tk.Label(new_window, image=img)
        img_label.image = img
        img_label.pack()

    def generate_report(self):
        new_window = tk.Toplevel()
        new_window.title("Report")
        label = tk.Label(new_window, text=self.plotter.generate_frame())
        label.pack()

    def start(self):
        return self.window.mainloop()
