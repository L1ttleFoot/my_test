from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,'my_app/index.html')#HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.
