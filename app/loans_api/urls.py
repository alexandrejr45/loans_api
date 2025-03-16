from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("simulate_loan/", include("loan_simulation.urls")),
    path("admin/", admin.site.urls),
]