from datetime import date

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

from settings import db_settings, db_echo, log_level
import logging

logger = logging.getLogger("database")
logger.setLevel(log_level)


engine = create_engine(db_settings.db_url, echo=db_echo)
Base = declarative_base()
session = Session(engine)


class Transaction(Base):
    __abstract__ = True

    id = Column("id", Integer, primary_key=True)
    amount = Column("amount", Float, nullable=False)
    description = Column("description", Text, nullable=True)
    date = Column("date", Date, default=date.today(), nullable=False)

    __table_args__ = (
        CheckConstraint(amount > 0, name="check_amount_positive"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "description": self.description,
            "date": self.date,
        }


class TransactionType(Base):
    __tablename__ = "transaction_types"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(50), nullable=False)

    __table_args__ = (UniqueConstraint(name, name="unique_name"),)


class Income(Transaction):
    __tablename__ = "incomes"

    type = Column(
        "type",
        Integer,
        ForeignKey("transaction_types.id"),
        default=1,
        nullable=False,
    )

    def to_dict(self):
        dic = super().to_dict()
        dic["table"] = "Income"
        return dic


class Expense(Transaction):
    __tablename__ = "expenses"

    type = Column(
        "type",
        Integer,
        ForeignKey("transaction_types.id"),
        default=2,
        nullable=False,
    )

    def to_dict(self):
        dic = super().to_dict()
        dic["amount"] = -dic["amount"]
        dic["table"] = "Expense"
        return dic


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    __table_args__ = (
        CheckConstraint(amount > 0, name="check_amount_positive"),
    )


Base.metadata.create_all(engine)

types = [TransactionType(name="Income"), TransactionType(name="Expense")]
try:
    insert_types = session.bulk_save_objects(types)
    session.commit()
except IntegrityError:
    session.rollback()
except AttributeError:
    session.rollback()
