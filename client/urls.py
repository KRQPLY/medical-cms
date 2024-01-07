from django.urls import path, include
from client import views

urlpatterns = [
    path('', views.page_view, name='page_client'),
    path("administration/", include("apps.authentication.urls")),
    path("administration/", include("apps.home.urls")),
    path('<str:page_name>/', views.page_view, name='page_client'),
    path('<str:page_name>/<path:pages_names>/', views.page_view, name='page_client_with_extra_params')
]
