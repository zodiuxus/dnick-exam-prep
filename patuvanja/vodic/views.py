from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("If you're seeing this, then the index page is working, and likely everything else (for now).")

def destinacii(request):
    return HttpResponse("Congrats, you're at the destinations page.")