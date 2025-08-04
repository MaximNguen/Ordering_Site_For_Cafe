from django.shortcuts import render
from CompanyText import Texts

def home(request):
    data = {"title": Texts.title}
    return render(request, 'home.html', context=data)
