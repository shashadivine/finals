from django.shortcuts import render

# Create your views here.

def openapp(request):
   return render (request, 'restoapp/base.html')