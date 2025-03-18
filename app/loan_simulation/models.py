import uuid
from dataclasses import dataclass
from decimal import Decimal
from datetime import date

@dataclass
class InterestRate:
    client_birthdate: date
    current_date: date = date.today()
    amount: Decimal = Decimal(0)


@dataclass
class LoanSimulation:
    amount: Decimal
    client_birthdate: date
    payment_period: int


@dataclass
class LoanSimulationResult:
    id: uuid.UUID
    total_amount: Decimal
    monthly_installment: Decimal
    interest_total_amount: Decimal
