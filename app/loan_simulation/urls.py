from django.urls import path

from loan_simulation import views

urlpatterns = [
    path("", views.index, name="index"),
]
