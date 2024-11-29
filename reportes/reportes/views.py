from django.shortcuts import render # type: ignore
from django.http import HttpResponse # type: ignore

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')

def healthCheck(request):
    return HttpResponse("OK")