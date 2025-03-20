from datetime import date
from decimal import Decimal

import pytest
from loan_simulation.enums import InterestRateByAge
from loan_simulation.helpers.calculate_simulations import (
    calculate_interest_rate,
    calculate_monthly_installments,
    get_interest_rate
)
from rest_framework.exceptions import ValidationError


class TestGetInterestRate:

    @pytest.mark.parametrize('client_age', [19, 25])
    def test_should_return_interest_tax_for_clients_less_or_equal_to_25_years(
        self,
        client_age
    ):
        interest_tax = get_interest_rate(client_age)

        assert interest_tax == InterestRateByAge.YOUNG.value

    @pytest.mark.parametrize('client_age', [33, 39])
    def test_should_return_interest_tax_for_clients_between_26_and_40_years(
        self,
        client_age
    ):
        interest_tax = get_interest_rate(client_age)

        assert interest_tax == InterestRateByAge.ADULT.value

    @pytest.mark.parametrize('client_age', [47, 56])
    def test_should_return_interest_tax_for_clients_between_41_and_60_years(
        self,
        client_age
    ):
        interest_tax = get_interest_rate(client_age)

        assert interest_tax == InterestRateByAge.OLD_ADULT.value

    @pytest.mark.parametrize('client_age', [64, 76])
    def test_should_return_interest_tax_for_clients_above_60_years(
        self,
        client_age
    ):
        interest_tax = get_interest_rate(client_age)

        assert interest_tax == InterestRateByAge.ELDERLY.value

    @pytest.mark.parametrize('client_age', [15, 120])
    def test_should_raise_an_error_when_the_client_age_is_not_valid(
        self,
        client_age
    ):
        with pytest.raises(ValidationError):
            get_interest_rate(client_age)


class TestCalculateMonthlyInstallments:

    def test_should_calculate_monthly_installments_with_interest_rate_equal_to_5_percent( # noqa
        self,
        loan_simulation_request_model
    ):
        monthly_installment = calculate_monthly_installments(
            loan_simulation_request_model
        )

        assert isinstance(monthly_installment, Decimal)
        assert monthly_installment == Decimal('543.86')

    def test_should_calculate_monthly_installments_with_interest_rate_equal_to_3_percent(  # noqa
            self,
            loan_simulation_request_model
    ):
        loan_simulation_request_model.user.birthdate = (
            date.fromisoformat('1990-02-04')
        )

        monthly_installment = calculate_monthly_installments(
            loan_simulation_request_model
        )

        assert isinstance(monthly_installment, Decimal)
        assert monthly_installment == Decimal('526.04')

    def test_should_calculate_monthly_installments_with_interest_rate_equal_to_2_percent(  # noqa
            self,
            loan_simulation_request_model
    ):
        loan_simulation_request_model.user.birthdate = (
            date.fromisoformat('1980-02-04')
        )

        monthly_installment = calculate_monthly_installments(
            loan_simulation_request_model
        )

        assert isinstance(monthly_installment, Decimal)
        assert monthly_installment == Decimal('517.27')

    def test_should_calculate_monthly_installments_with_interest_rate_equal_to_4_percent(  # noqa
            self,
            loan_simulation_request_model
    ):
        loan_simulation_request_model.user.birthdate = (
            date.fromisoformat('1960-02-04')
        )

        monthly_installment = calculate_monthly_installments(
            loan_simulation_request_model
        )

        assert isinstance(monthly_installment, Decimal)
        assert monthly_installment == Decimal('534.91')


class TestCalculateInterestRate:

    def test_should_return_a_young_interest_rate_using_client_birthdate(self):
        client_birthdate = date.fromisoformat('1999-09-02')

        assert calculate_interest_rate(client_birthdate) == (
            InterestRateByAge.YOUNG.value
        )

    def test_should_return_a_adult_interest_rate_using_client_birthdate(self):
        client_birthdate = date.fromisoformat('1990-09-02')

        assert calculate_interest_rate(client_birthdate) == (
            InterestRateByAge.ADULT.value
        )

    def test_should_return_a_old_adult_interest_rate_using_client_birthdate(
        self
    ):
        client_birthdate = date.fromisoformat('1980-09-02')

        assert calculate_interest_rate(client_birthdate) == (
            InterestRateByAge.OLD_ADULT.value
        )

    def test_should_return_a_elderly_interest_rate_using_client_birthdate(
        self
    ):
        client_birthdate = date.fromisoformat('1960-09-02')

        assert calculate_interest_rate(client_birthdate) == (
            InterestRateByAge.ELDERLY.value
        )
