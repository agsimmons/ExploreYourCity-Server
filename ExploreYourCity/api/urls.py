from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='register'),
    path('missions/', views.Missions.as_view(), name='missions'),
    path('missions/<int:pk>/', views.MissionsDetail.as_view(), name='missions_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
