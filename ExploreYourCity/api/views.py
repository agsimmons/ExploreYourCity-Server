from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello, World! This is the index view for the api!')

