# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("client.urls")),
    path("administration/", include("apps.authentication.urls")),
    path("administration/", include("apps.home.urls"))
]
