"""bobtex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import library.urls
from library.views import show_all, delete, full_tex, delete_maybe

urlpatterns = [
                  path('delete-maybe/<slug:id>', delete_maybe),
                  path('delete/<slug:id>', delete),
                  path('bibtex', full_tex),
                  path('', show_all),

              ] + static('uploads', document_root='uploads')
