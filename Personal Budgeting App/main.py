from handlers import TransactionExpense, TransactionIncome

import logging

from GUI import BudgetApp
from settings import log_level

logger = logging.getLogger("main")
logger.setLevel(log_level)


def main():
    while True:
        try:
            app = BudgetApp()
            app.start()
        except Exception as e:
            logger.error(e)
            print(e)
            # continue
            break


if __name__ == "__main__":
    main()
