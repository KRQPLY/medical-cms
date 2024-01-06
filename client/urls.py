from django.urls import path
from client import views

urlpatterns = [
    path('', views.page_view, name='home_client'),
    path('<str:page_name>', views.page_view, name='home_client')
]
