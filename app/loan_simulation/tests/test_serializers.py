from datetime import date
from decimal import Decimal

from loan_simulation.serializers import LoanSimulationSerializer


class TestSerializers:

    def test_should_return_validated_loan_simulation_dict(
        self,
        loan_simulation_payload
    ):
        data = loan_simulation_payload
        serializer = LoanSimulationSerializer(data=data)

        assert serializer.is_valid()
        assert serializer.validated_data['amount'] == Decimal(data['amount'])
        assert serializer.validated_data['user']['birthdate'] == (
            date.fromisoformat(data['user']['birthdate'])
        )
        assert serializer.validated_data['payment_period'] == (
            data['payment_period']
        )
