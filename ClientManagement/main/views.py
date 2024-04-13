from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "generic.html")

def litigation_new(request):
    return render(request, "main/litigation_new.html")
