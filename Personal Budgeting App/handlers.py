import logging
from datetime import date

from sqlalchemy.orm import Session

from settings import log_level
from database import Goal, Expense, Income, session
from random import randint

logger = logging.getLogger("handler")
logger.setLevel(log_level)


class DBTransaction:
    def __init__(self, model: Income | Expense, session: Session = session):
        self.session = session
        self.model = model

    def create(self, values: dict) -> Expense | Income:
        self.session.add(self.model(**values))
        self.session.commit()

    def update(self, values: dict, id: int):
        self.session.query(self.model).filter_by(id=id).update(values)
        self.session.commit()

    def delete(self, id: int):
        self.session.query(self.model).filter_by(id=id).delete()
        self.session.commit()

    def delete_all(self):
        self.session.query(self.model).delete()
        self.session.commit()

    def get(self, id: int) -> Expense | Income:
        return self.session.query(self.model).filter_by(id=id).first()

    def get_all(self) -> list[Expense | Income]:
        return self.session.query(self.model).all()


class TransactionIncome(DBTransaction):
    def __init__(self, session: Session = session):
        super().__init__(Income, session)


class TransactionExpense(DBTransaction):
    def __init__(self, session: Session = session):
        super().__init__(Expense, session)


class TransactionGoal(DBTransaction):
    def __init__(self, session: Session = session):
        super().__init__(Goal, session)
        
def fill_db(n=10000):
    year = 2022
    n_day = 365
    income = TransactionIncome()
    expense = TransactionExpense()
    #empty
    income.delete_all()
    expense.delete_all()
    
    ordinal_start = date(2022,1,1).toordinal()
    logger.info("start generating random data")
    for x in range(n):
        logger.info(f"data {x}")
        day = ordinal_start+randint(0,n_day-1)
        amount = randint(-500,500)
        if amount > 0:
            income.create({
                "amount":amount,
                "description": f"description {x}",
                "date": date.fromordinal(day),
            })
        elif amount < 0:
            expense.create({
                "amount":-amount,
                "description": f"description {x}",
                "date": date.fromordinal(day),
            })

if __name__ == "__main__":
    """Test"""
    fill_db()
    exit()
    goal = TransactionGoal()
    income = TransactionIncome()
    expense = TransactionExpense()
    income.create(
        {
            "amount": 100,
            "description": "test_income_1",
            "date": date(2021, 2, 1),
        }
    )
    expense.create(
        {
            "amount": 100,
            "description": "test_expense_1",
            "date": date(2021, 2, 1),
        }
    )
    income.create(
        {
            "amount": 100,
            "description": "test_income_2",
            "date": date(2021, 2, 1),
        }
    )
    income.create(
        {
            "amount": 100,
            "description": "test_income_2",
            "date": date(2023, 2, 1),
        }
    )
    expense.create(
        {
            "amount": 100,
            "description": "test_expense_2",
            "date": date(2021, 2, 1),
        }
    )
    expense.create(
        {
            "amount": 100,
            "description": "test_expense_2",
            "date": date(2022, 2, 1),
        }
    )
    print(income.get(id=1).description)
    print(expense.get(id=1).description)
    income.update({"description": "test_income_1_updated"}, id=1)
    expense.update({"description": "test_expense_1_updated"}, id=1)
    print(income.get(id=1).description)
    print(expense.get(id=1).description)
    print(income.get_all())
    print(expense.get_all())