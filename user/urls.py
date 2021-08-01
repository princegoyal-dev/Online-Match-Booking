from django.urls import path
from user import views
from django.conf.urls import url

urlpatterns = [
    url(r'^login/', views.user_login),
    url(r'^signup/', views.user_signup),
    url(r'^match_reg/', views.join_match),
    url(r'^handlerequest/', views.handlerequest),
    url(r'^paymenthistory/', views.paymenthistory),
    url(r'^aboutus/', views.aboutus),
    url(r'^contactus/', views.contactus),
    url(r'^(?P<username>.+)/$', views.profile_login),
]
