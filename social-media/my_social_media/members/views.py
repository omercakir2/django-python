# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import MemberRegistrationForm, MemberLoginForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator


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
    return render(request,'main.html')

def register_view(request):
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            messages.success(request, 'Please confirm your email address to complete the registration.')
            return redirect('/')  # Replace 'home' with your desired redirect URL name
    else:
        form = MemberRegistrationForm()
    return render(request, 'register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Member.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Member.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated!')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('registration_complete')

def login_view(request):
    if request.method == 'POST':
        form = MemberLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            context = {
            'user':user,
            }
            if user is not None:
                login(request, user)
                messages.success(request,'You are succesfully loged in')
                return redirect('/',context)  
            
    else:
        form = MemberLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request,'Loged out successfully')
    return redirect('/')
    
def success_view(request):
    return render (request,'success.html')

# members/views.py


