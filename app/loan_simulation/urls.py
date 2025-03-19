from django.urls import path

from loan_simulation import views

urlpatterns = [
    path(
        'simulate-loan/',
        views.SimulateLoanView.as_view(),
        name='simulate_loan'
    ),
]
