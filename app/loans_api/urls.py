from django.contrib import admin
from django.urls import include, path

from loan_simulation.views import CreateToken

urlpatterns = [
    path('', include('loan_simulation.urls')),
    path('auth-token/', CreateToken.as_view()),
    path('admin/', admin.site.urls),
]
