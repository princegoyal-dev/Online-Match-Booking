from django.urls import path
from home import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.home_view),
]
