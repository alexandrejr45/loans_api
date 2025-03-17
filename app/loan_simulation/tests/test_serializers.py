import pytest

from decimal import Decimal
from datetime import date

from loan_simulation.serializers import LoanSimulationSerializer

class TestSerializers:

    @pytest.fixture
    def loan_simulation_payload(self):
        return {
            'amount': '1000000',
            'client_birthdate': '2000-02-12',
            'payment_period': 23
        }

    def test_should_return_validated_loan_simulation_dict(
        self,
        loan_simulation_payload
    ):
        data = loan_simulation_payload
        serializer = LoanSimulationSerializer(data=data)

        assert serializer.is_valid()
        assert serializer.validated_data['amount'] == Decimal(data['amount'])
        assert serializer.validated_data['client_birthdate'] == date.fromisoformat(data['client_birthdate'])
        assert serializer.validated_data['payment_period'] == data['payment_period']