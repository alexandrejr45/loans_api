from datetime import date
from decimal import Decimal

import pytest
from loan_simulation.models.dataclasses import LoanSimulationRequest, User


@pytest.fixture
def loan_simulation_payload():
    return {
        'amount': '10000',
        'user': {
            'name': 'José',
            'last_name': 'Silva',
            'document_number': '01234567890',
            'birthdate': '2000-02-21'
        },
        'payment_period': 24
    }


@pytest.fixture
def loan_simulation_request_model(loan_simulation_payload):
    return LoanSimulationRequest(
        amount=Decimal('20000'),
        user=User(
            name='Xablau',
            last_name='Fulano',
            document_number='01234567890',
            birthdate=date.fromisoformat('1999-08-23')
        ),
        payment_period=40
    )
