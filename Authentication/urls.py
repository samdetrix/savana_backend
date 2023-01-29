from django.urls import path, include

from Authentication.views import *

urlpatterns = [
    path('users/', GetAllCustomerAPIView.as_view(), name='users'),
    path('register/', CustomerRegisterView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('single-user/', PersonnelQueryView.as_view(), name='single-users'),
]