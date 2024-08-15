# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import MemberRegistrationForm, MemberLoginForm

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

def register_view(request):
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')  # Replace 'home' with your desired redirect URL name
    else:
        form = MemberRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = MemberLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Replace 'home' with your desired redirect URL name
    else:
        form = MemberLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')
    


