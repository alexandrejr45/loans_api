from rest_framework import serializers

from loan_simulation.models import LoanSimulation


class LoanSimulationSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    client_birthdate = serializers.DateField()
    payment_period = serializers.IntegerField()


    def create(self, validated_data):
        return LoanSimulation(**validated_data)