from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

def index(request):
    print("App is running under the pools app tara ..... ")
    return HttpResponse("Hello, world. You're at the polls index.")