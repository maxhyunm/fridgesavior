from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'users'

urlpatterns = [
    # path('google/login', google_login, name='google_login'),
    # path('google/callback/', google_callback, name='google_callback'),
    # path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
    path('kakao/login/', kakao_login, name='kakao-login'),
    path('kakao/callback/', kakao_callback, name='kakao-callback'),
    # path('kakao/login/finish/', KakaoLogin.as_view(), name='kakao_login_todjango'),
]
