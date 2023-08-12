from django.shortcuts import render

def index(request):
    return render(request,'template/index.html')

def about(request):
    return render(request,'template/about.html')