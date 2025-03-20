from datetime import date

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from validate_docbr import CNPJ, CPF

from loan_simulation.models.dataclasses import LoanSimulationRequest, User


class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=100)
    document_number = serializers.CharField(max_length=14)
    birthdate = serializers.DateField()

    def validate_document_number(self, value):
        if len(value) == 11:
            cpf_validator = CPF()
            if cpf_validator.validate(cpf_validator.mask(value)):
                return value
        elif len(value) == 14:
            cnpj_validator = CNPJ()
            if cnpj_validator.validate(cnpj_validator.mask(value)):
                return value

        raise ValidationError('User document_number is invalid')

    def validate_birthdate(self, value):
        total_days = (date.today() - value)
        client_age = int(total_days.days / 365)

        if client_age < 18:
            raise ValidationError('User age is less than 18 years')
        elif client_age > 100:
            raise ValidationError('User age is above than 100 years')

        return value


class LoanSimulationSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    payment_period = serializers.IntegerField()
    user = UserSerializer()

    def create(self, validated_data):
        return LoanSimulationRequest(
            amount=validated_data['amount'],
            payment_period=validated_data['payment_period'],
            user=User(
                name=validated_data['user']['name'],
                last_name=validated_data['user']['last_name'],
                document_number=validated_data['user']['document_number'],
                birthdate=validated_data['user']['birthdate']
            )
        )
