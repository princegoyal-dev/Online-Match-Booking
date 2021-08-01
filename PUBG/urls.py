"""PUBG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import include,url
from django.urls import path
from home import urls as homeurls
from django.views.generic import RedirectView
from django.contrib import admin
from user import urls as userurls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',include(homeurls)),
    path('user/',include(userurls)),
    url(r'^$', RedirectView.as_view(url='/home')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
