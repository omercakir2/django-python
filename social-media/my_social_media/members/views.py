# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def members(request):
  template = loader.get_template('firsthtml.html')
  return HttpResponse(template.render())


