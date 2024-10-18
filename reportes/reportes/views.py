from django.shortcuts import render # type: ignore
from django.http import HttpResponse # type: ignore

def home(request):
    return HttpResponse("Hello world! Django views")

def index(request):
    return render(request, 'index.html')

def healthCheck(request):
    return HttpResponse("OK")