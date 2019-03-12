from django.urls import path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from . import views

urlpatterns = [
    path('docs/', include_docs_urls(title='ExploreYourCity')),
]

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'players', views.PlayerViewSet)
router.register(r'missions', views.MissionViewSet)
router.register(r'objectives', views.ObjectiveViewSet)
router.register(r'requests', views.RequestViewSet, basename='request')
urlpatterns = urlpatterns + router.urls
