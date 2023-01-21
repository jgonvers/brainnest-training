from handlers import TransactionExpense, TransactionIncome

from settings import log_level
import logging
logger = logging.getLogger("main")
logger.setLevel(log_level)


def main():
    income = TransactionIncome()
    expense = TransactionExpense()
