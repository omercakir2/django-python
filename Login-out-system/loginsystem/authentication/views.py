from django.shortcuts import render,redirect
from django.template import loader 
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request,"Your account is succesfully created !")
        return redirect('signin')

    #template = loader.get_template('signup.html')
    #return HttpResponse(template.render())
    return render(request,"signup.html")
def signin(request):
    #template = loader.get_template('signin.html')
    #return HttpResponse(template.render())
    return render(request,"signin.html")
def signout(request):
    #template = loader.get_template('signout.html')
    #return HttpResponse(template.render())
    return render(request,"signout.html")
    