from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home_admin'),
    path('pages/<int:pk>', views.components_view, name='components_admin'),
    path('pages', views.pages_view, name='pages_admin'),
    path('components/all', views.components_all_view, name='components_all_admin'),
    path('components/browse/<str:model_name>', views.components_browse_view, name='components_browse_admin'),
    path('components/edit/<str:model_name>/<int:pk>', views.edit_object, name='edit_object_admin'),
    path('components/delete/<str:model_name>/<int:pk>', views.delete_object, name='delete_object_admin'),
    path('components/add/<str:model_name>', views.add_object, name='add_object_admin'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
