import pytest

from decimal import Decimal
from math import pow

from loan_simulation.helpers import (
    get_interest_rate,
    calculate_monthly_installments,
    calculate_interest_rate
)
from loan_simulation.enums import InterestRateByAge


class TestGetInterestRate:

    @pytest.mark.parametrize('client_age', [19, 25])
    def test_should_return_interest_tax_for_clients_less_or_equal_to_25_yeas(
        self,
        client_age
    ):
        interest_tax = get_interest_rate(client_age)

        assert interest_tax == InterestRateByAge.YOUNG.value


class TestCalculateMonthlyInstallments:

    def calculate_monthly_installment(
        self,
        loan_dict: dict
    ):
        interest_rate = calculate_interest_rate(
            loan_dict['client_birthdate']
        ) / 12
        return Decimal(
            (loan_dict['amount'] * interest_rate) /
            Decimal(1 - pow(1 + interest_rate, -loan_dict['payment_period']))
        ).quantize(Decimal('0.00'))

    def test_should_calculate_monthly_installments_with_valid_loan(
        self,
        loan_simulation_payload
    ):
        monthly_installment = calculate_monthly_installments(
            loan_simulation_payload
        )

        assert monthly_installment == self.calculate_monthly_installment(
            loan_simulation_payload
        )
