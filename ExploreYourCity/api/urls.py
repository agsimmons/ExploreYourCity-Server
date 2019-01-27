from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('register_user/', views.UserRegister.as_view(), name='register_user'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
