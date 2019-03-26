from django.urls import path
from django.http import HttpResponse

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('robots.txt',
         lambda x: HttpResponse("User-Agent: *\nDisallow: /", content_type="text/plain"),
         name="robots_file"),
]

