import enum


class TransactionType(enum.Enum):
    Income = "Income"
    Expense = "Expense"


class StatusType(enum.Enum):
    Nil = "Nil"
    Cleared = "Cleared"
    Reconciled = "Reconciled"
    Void = "Void"
