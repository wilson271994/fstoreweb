from django.urls import re_path
from .views import *

app_name = "core"

urlpatterns = [
    re_path(r'^auth-home$', AuthHome, name="auth-home"),
    re_path(r'^auth-creation$', CreateUser, name="auth-creation"),
    re_path(r'^auth-login$', userLoginMethod, name='auth-login'),
    re_path(r'^auth-activation$', accountActivationMethod, name="auth-activation" ),
    re_path(r'^auth-logout$', userLogOut, name='auth-logout'),
    re_path(r'^country-cities$', getCityFromCountry, name='country-cities'),
]