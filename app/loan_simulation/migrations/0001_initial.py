# Generated by Django 5.1.7 on 2025-03-21 05:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=100)),
                ('document_number', models.CharField(max_length=14, unique=True)),
                ('birthdate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='LoanSimulation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('simulation_id', models.UUIDField(db_index=True, unique=True)),
                ('monthly_installment', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_interest_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loan_simulation.customer')),
            ],
        ),
    ]
