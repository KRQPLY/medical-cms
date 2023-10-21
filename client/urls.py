from django.urls import path, re_path
from client import views

urlpatterns = [
    # The home page
    path('', views.home_view, name='home_client'),
    path('home/', views.home_view, name='home_client'),
    path('error/', views.error_view, name='error'),
    path('blog/', views.blog_view, name='blog'),
    path('contact/', views.contact_view, name='contact'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
]
