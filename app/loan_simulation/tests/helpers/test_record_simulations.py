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
        save_customer_model(loan_simulation_response_model.user)
        save_customer_model(loan_simulation_response_model.user)

        assert len(Customer.objects.all()) == 1


class TestSaveLoanSimulation:

    def test_should_save_a_loan_simulation(
        self,
        loan_simulation_response_model
    ):
        response_model = loan_simulation_response_model
        save_loan_simulation(response_model)
        saved_simulation = LoanSimulation.objects.all().first()

        assert saved_simulation.simulation_id == response_model.id
        assert saved_simulation.monthly_installment == (
            response_model.monthly_installment
        )
        assert saved_simulation.total_amount == response_model.total_amount
        assert saved_simulation.total_interest_amount == (
            response_model.total_interest_amount
        )

        assert saved_simulation.user.name == response_model.user.name
        assert saved_simulation.user.last_name == response_model.user.last_name
        assert saved_simulation.user.document_number == (
            response_model.user.document_number
        )
        assert saved_simulation.user.birthdate == response_model.user.birthdate
