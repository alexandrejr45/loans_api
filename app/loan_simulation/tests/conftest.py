from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest

from loan_simulation.models.dataclasses import (
    LoanSimulationRequest,
    LoanSimulationResponse,
    User
)


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


@pytest.fixture
def loan_simulation_response_model(loan_simulation_payload):
    return LoanSimulationResponse(
        id=uuid4(),
        user=User(
            name='Xablau',
            last_name='Fulano',
            document_number='01234567890',
            birthdate=date.fromisoformat('1999-08-23')
        ),
        monthly_installment=Decimal('534.86'),
        total_interest_amount=Decimal('1394.40'),
        total_amount=Decimal('534.86')*40
    )
