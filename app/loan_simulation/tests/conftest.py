import pytest


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
