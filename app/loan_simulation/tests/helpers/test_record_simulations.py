from copy import deepcopy
from unittest.mock import patch

import pytest

from loan_simulation.helpers.record_simulations import (
    save_customer_model,
    save_loan_simulation
)
from loan_simulation.models.loan_simulation import Customer, LoanSimulation

pytestmark = pytest.mark.django_db


class TestSaveCustomerModel:

    def test_should_save_a_customer_model(
        self,
        loan_simulation_response_model
    ):
        customer = save_customer_model(loan_simulation_response_model.user)

        assert customer == Customer.objects.all().first()

    def test_should_not_save_a_costumer_if_he_already_exists(
        self,
        loan_simulation_response_model
    ):
        with patch('loan_simulation.models.loan_simulation.Customer.save') as (
            mock_customer
        ):
            save_customer_model(loan_simulation_response_model.user)
            save_customer_model(loan_simulation_response_model.user)

        mock_customer.assert_called_once()

class TestSaveLoanSimulation:

    def test_should_save_a_loan_simulation(
        self,
        loan_simulation_response_model
    ):
        simulation = save_loan_simulation(loan_simulation_response_model)

        assert simulation == LoanSimulation.objects.all().first()
