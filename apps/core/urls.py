from django.urls import path
from . import views  # Import views here

urlpatterns = [
    path('', views.home, name='home'),
]
