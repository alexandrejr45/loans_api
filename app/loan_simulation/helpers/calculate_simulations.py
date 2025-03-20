from datetime import date
from decimal import Decimal
from math import pow
from uuid import uuid4

from loan_simulation.enums import InterestRateByAge
from loan_simulation.models.dataclasses import (
    LoanSimulationRequest,
    LoanSimulationResponse
)
from rest_framework.exceptions import ValidationError


def calculate_loan_simulation(
    loan_simulation: LoanSimulationRequest
) -> LoanSimulationResponse:
    monthly_installment = calculate_monthly_installments(loan_simulation)
    total_amount = Decimal(
        monthly_installment * loan_simulation.payment_period
    )
    total_interest_amount = Decimal(total_amount - loan_simulation.amount)

    return LoanSimulationResponse(
        id=uuid4(),
        monthly_installment=monthly_installment,
        total_amount=total_amount,
        total_interest_amount=total_interest_amount,
        user=loan_simulation.user
    )


def calculate_monthly_installments(
    loan_simulation: LoanSimulationRequest
) -> Decimal:
    interest_rate = calculate_interest_rate(
        loan_simulation.user.birthdate
    ) / 12
    loan_amount = loan_simulation.amount
    monthly_installment = Decimal(
        (loan_amount * interest_rate) /
        Decimal(1 - pow(1 + interest_rate, -loan_simulation.payment_period))
    ).quantize(Decimal('0.00'))

    return monthly_installment


def calculate_interest_rate(client_birthdate: date) -> Decimal:
    total_days = (date.today() - client_birthdate)
    client_age = int(total_days.days / 365)

    return get_interest_rate(client_age)


def get_interest_rate(client_age: int) -> Decimal:
    tax_map = {
        (17, 25): InterestRateByAge.YOUNG.value,
        (25, 40): InterestRateByAge.ADULT.value,
        (40, 60): InterestRateByAge.OLD_ADULT.value,
        (60, 100): InterestRateByAge.ELDERLY.value
    }

    for age_range, tax in tax_map.items():
        if age_range[0] < client_age <= age_range[1]:
            return tax

    raise ValidationError('Client age is not in a valid interval')
