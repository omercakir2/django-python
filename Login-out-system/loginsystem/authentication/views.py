import re
from django.shortcuts import render,redirect
from django.template import loader 
from django.http import HttpResponse
from django.contrib.auth.models import User #it is a ready-to-use data structure
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.http import Http404
from django.views import View

class VerifyEmail(View):
    def get(self, request, user_id, verification_code):
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id, verification_code=verification_code)
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return redirect('login')  # or redirect to a success page
            else:
                return redirect('login')  # or some page indicating already verified
        except User.DoesNotExist:
            raise Http404('User does not exist.')


def send_verification_email(user):
    verification_link = reverse('verify_email', args=[user.pk, user.verification_code])
    verification_url = f'http://127.0.0.1:8000/{verification_link}'
    subject = 'Verify Your Email Address'
    html_message = render_to_string('verification_email.html', {'user': user, 'verification_link': verification_url})
    send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)


def home(request):
    template = loader.get_template('home.html')
    #return HttpResponse(template.render())
    return render(request,"home.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request,"This username is already used by someone else")
            return redirect('home')
        if User.objects.filter(email=email):
            messages.error(request,"This e-mail is already used by someone else")
            return redirect('home')
        if len(username)>10:
            messages.error(request,"Username must consist of 10 letters maximum")
            return redirect('home')
        if pass1 != pass2 :
            messages.error(request,"The passwords do not match")
            return redirect('home')
            

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        send_verification_email(myuser)
        return redirect('registiration_complate')

        messages.success(request,"Your account is succesfully created !")
        return redirect('signin')

    #template = loader.get_template('signup.html')
    #return HttpResponse(template.render())
    return render(request,"signup.html")
def signin(request):
    #template = loader.get_template('signin.html')
    #return HttpResponse(template.render())
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username,password=pass1)#checks username given matches with password
        if user is not None:
                login(request,user) 
                fname = user.get_username()
                messages.success(request,"You logged in succesfully")
                return render(request,"home.html",{'fname' : fname})  
        else:
            messages.error(request,"Not matched")
            return redirect('home')
            #return render(request,'home.html')
    return render(request,"signin.html") 
def signout(request):
    #template = loader.get_template('signout.html')
    #return HttpResponse(template.render())
    logout(request)
    messages.success(request,'Logged out succesfully')  
    return redirect('home')
def profile(request):
    Users = User.objects.all().values()
    
    return render(request,"profile.html",{'Users':Users})