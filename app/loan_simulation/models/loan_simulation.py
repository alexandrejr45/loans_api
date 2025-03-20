from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    document_number = models.CharField(max_length=14, unique=True)
    birthdate = models.DateField()


class LoanSimulation(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    simulation_id = models.UUIDField()
    monthly_installment = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    total_interest_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
