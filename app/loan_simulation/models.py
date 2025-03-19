import uuid
from dataclasses import dataclass
from decimal import Decimal
from datetime import date


@dataclass
class User:
    name: str
    last_name: str
    document_number: str
    birthdate: date


@dataclass
class LoanSimulationRequest:
    amount: Decimal
    payment_period: int
    user: User


@dataclass
class LoanSimulationResponse:
    id: uuid.UUID
    monthly_installment: Decimal
    total_amount: Decimal
    total_interest_amount: Decimal
    user: User

    def __post_init__(self):
        self.total_amount = Decimal(
            self.total_amount
        ).quantize(Decimal('0.00'))
        self.monthly_installment = Decimal(
            self.monthly_installment
        ).quantize(Decimal('0.00'))
        self.total_interest_amount = Decimal(
            self.total_interest_amount
        ).quantize(Decimal('0.00'))
