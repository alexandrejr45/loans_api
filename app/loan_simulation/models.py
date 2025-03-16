from dataclasses import dataclass
from decimal import Decimal
from datetime import date


@dataclass
class InterestTax:
    client_birthdate: date
    current_date: date = date.today()
    amount: Decimal = Decimal(0)


@dataclass
class LoanSimulation:
    amount: Decimal
    client_birthdate: date
    payment_period: int
    interest_tax: Decimal = Decimal(0)


@dataclass
class LoanSimulationResult:
    total_amount: Decimal
    monthly_installment: Decimal
    interest_total_amount: Decimal


