from django.urls import path, include
from density import views

urlpatterns = [
    path('', views.home, name='home'),
]
