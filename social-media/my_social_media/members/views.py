# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member
def members(request):
  members = Member.objects.all().values()    
  template = loader.get_template('allmembers.html')
  context = {
      'mymembers':members,
  }
  return HttpResponse(template.render(context,request))

def details(request,id):
    mymember = Member.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'mymember':mymember,
    }
    return HttpResponse(template.render(context,request))

def home(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())
    


