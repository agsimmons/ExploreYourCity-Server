from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from . import views

urlpatterns = [
    path('docs/', include_docs_urls(title='ExploreYourCity')),
]

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'missions', views.MissionViewSet)
urlpatterns = urlpatterns + router.urls