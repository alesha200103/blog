from django.urls import path

from .views import api_registration

urlpatterns = [
    path("", api_registration),
]