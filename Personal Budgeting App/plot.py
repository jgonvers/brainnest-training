import pandas as pd
import numpy as np
import logging
from datetime import datetime as date
from tempfile import gettempdir
from os.path import join, exists
import matplotlib.pyplot as plt
from random import randrange
from os import makedirs

from settings import log_level
from handlers import TransactionIncome, TransactionExpense, TransactionGoal

logger = logging.getLogger("plot")
logger.setLevel(log_level)


class Plotter:
    def __init__(self):
        self.income = TransactionIncome()
        self.expense = TransactionExpense()
        self.goal = TransactionGoal()
        self.temp_dir = join(gettempdir(), "budgetingapp")
        if not exists(self.temp_dir):
            makedirs(self.temp_dir)

    def generate_bar_plot(
        self, size_x=500, size_y=500, by="day", window=None, width=10
    ):

        dpi = 100
        figsize = (size_x / dpi, size_y / dpi)

        ##modify if adding an windows (from x to y )
        if window is None or True:
            income = list(map(lambda x: x.to_dict(), self.income.get_all()))
            expense = list(map(lambda x: x.to_dict(), self.expense.get_all()))
        else:
            pass  # use a getter for the window

        income = self._sum_by(income, by)
        in_x = [x[0] for x in income]
        in_y = [x[1] for x in income]
        expense = self._sum_by(expense, by)
        expense = [(x[0], -x[1]) for x in expense]
        ex_x = [x[0] for x in expense]
        ex_y = [x[1] for x in expense]

        fig, ax = plt.subplots()
        fig.set_size_inches(*figsize)
        fig.set_dpi(dpi)
        rects1 = ax.bar(
            in_x,
            in_y,
            label="Income",
            color="green",
            width=width,
            align="edge",
        )
        rects2 = ax.bar(
            ex_x,
            ex_y,
            label="Expense",
            color="red",
            width=-width,
            align="edge",
        )
        ax.set_ylabel("Amount")
        ax.set_xlabel("Date")
        ax.legend()
        ax.xaxis_date()
        location = join(
            self.temp_dir, "figure{}.png".format(randrange(int(1e20)))
        )
        plt.savefig(location)
        return location

    def generate_frame(self):
        return self._create_frame(
            map(
                lambda x: x.to_dict(),
                self.expense.get_all() + self.income.get_all(),
            )
        )

    def _create_frame(self, transactions_list):
        return pd.DataFrame.from_dict(transactions_list)

    def _sum_by(self, dict_list, by="day"):
        if by == "month":
            format = "%Y-%m"
        elif by == "year":
            format = "%Y"
        else:
            format = "%Y-%m-%d"
        grouped = {}
        for tr in dict_list:
            key = tr["date"].strftime(format)
            if key in grouped:
                grouped[key] += tr["amount"]
            else:
                grouped[key] = tr["amount"]
        return [
            (
                date.strptime(key, format),
                value,
            )
            for (key, value) in grouped.items()
        ]


if __name__ == "__main__":
    pl = Plotter()
    print(pl.generate_bar_plot(1000, 800, by="day", width=10))
    print(pl.generate_frame())
