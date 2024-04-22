from django.shortcuts import render
from django.template import loader 
from django.http import HttpResponse

# Create your views here.
def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def signup(request):
    template = loader.get_template('signup.html')
    return HttpResponse(template.render())
def signin(request):
    template = loader.get_template('signin.html')
    return HttpResponse(template.render())
def signout(request):
    template = loader.get_template('signout.html')
    return HttpResponse(template.render())
    