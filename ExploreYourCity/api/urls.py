from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='register'),
    path('missions/', views.Missions.as_view(), name='missions'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
