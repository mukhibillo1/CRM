from django.urls import path
from . import views

app_name = "reception"

urlpatterns = [
    path('', views.ReceptionHomeView.as_view(), name="home"),
]
