import pytest

from decimal import Decimal
from datetime import date

@pytest.fixture
def valid_loan_simulation_dict():
    return {
        'amount': Decimal('10000'),
        'client_birthdate': date.fromisoformat('2000-12-09'),
        'payment_period': 60
    }