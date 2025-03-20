from django.db import transaction

from loan_simulation.models.dataclasses import LoanSimulationResponse, User
from loan_simulation.models.loan_simulation import Customer, LoanSimulation


def save_customer_model(user: User) -> Customer:
    saved_customer= search_customer_by_document_number(user)

    if saved_customer:
        return saved_customer

    customer = Customer(
        name=user.name,
        last_name=user.last_name,
        document_number=user.document_number,
        birthdate=user.birthdate
    )

    customer.save()

    return customer


def save_loan_simulation(
    loan_simulation: LoanSimulationResponse
) -> LoanSimulation:
    with transaction.atomic():
        saved_customer = save_customer_model(loan_simulation.user)

        simulation = LoanSimulation(
            user=saved_customer,
            simulation_id=loan_simulation.id,
            monthly_installment=loan_simulation.monthly_installment,
            total_amount=loan_simulation.total_amount,
            total_interest_amount=loan_simulation.total_interest_amount
        )
        simulation.save()

        return simulation


def search_customer_by_document_number(user: User) -> Customer | None:
    customer = Customer.objects.filter(
        document_number__exact=user.document_number
    )

    if customer:
        return customer
    return None

