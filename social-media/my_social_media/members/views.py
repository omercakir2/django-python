# Create your views here.
from re import template
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Friendship, Member
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
from pathlib import Path
from django.db.models import Q


def members(request):
    if 'search_req' in request.GET:
        search = request.GET['search_req']
        multiple_q = Q(Q(first_name__icontains=search) | Q(last_name__icontains=search))
        data = Member.objects.filter(multiple_q)
    else:
        data = Member.objects.all()
    context = {
      'mymembers':data,
    }
    return render(request,'allmembers.html',context)


def details(request,id):
    mymember = Member.objects.get(id=id)
    #followers=mymember.followers.all()
    followers = Friendship.objects.filter(to_user=mymember).values_list('from_user', flat=True)
    following=mymember.following.all()
    follower_count = mymember.followers.count()
    following_count = mymember.following.count()
    
    #is_following = Friendship.objects.filter(from_user=request.user, to_user=mymember).exists()

    if request.method=='POST':
        action = request.POST.get("action")
        if action == "add_friend":
            return follow_user(request,mymember.id)
        elif action == "remove_friend":
            return unfollow_user(request,mymember.id)
        else:
            pp = request.FILES.get('profile_picture')
            mymember.profile_picture=pp
            mymember.save()
            
    template = loader.get_template('details.html')
    context = {
        #'is_following':is_following,
        'followers':followers,
        'following':following,
        'followers_count':follower_count,
        'following_count':following_count,
        'mymember':mymember,
        'logged_in_user': request.user,#to get the user who's loged in at the moment
        
    }
    return HttpResponse(template.render(context,request))

def edit_view(request,id):
    currentmember = Member.objects.get(id=id)
    if request.user != currentmember:
        messages.error(request,'You are not allowed to change ')
        #return redirect('/')
        return redirect('details',id=id) 

    if request.method=='POST':
        try:
            currentmember.first_name = request.POST.get('first_name')
            currentmember.last_name = request.POST.get('last_name')
            currentmember.save()
            messages.success(request,'You are successfully changed your informations')
        except:
            messages.error('Something went wrong. Please try again')    
    context = {
        'user':currentmember
    }
    return render(request,'edit.html',context)
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

def forget_password_view(request):
    if request.method=='POST':
        email = request.POST.get('email')
        if Member.objects.filter(email=email).exists():
            user = Member.objects.get(email=email)
            messages.success(request,'We have send you a link to reset your password')
            current_site = get_current_site(request)
            mail_subject = 'Reset Password'
            message = render_to_string('reset_pass.html', {
                'email': email,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])            
        else:
            messages.error(request,'The e-mail you typed does not belong to any user.')
            

    return render(request, 'forgetpassword.html')        
        
def reset_password_view(request, uidb64, token):
    # Decode the UID from base64
    uid = urlsafe_base64_decode(uidb64).decode()
        # Fetch the user from the UID
    user = Member.objects.get(pk=uid)
    message ={
        'user':user
    }
    if request.method=='POST':
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if pass1==pass2:
            user.set_password(pass1)
            user.save()
            messages.success(request,'You are successfully changed your password')
            
        else:
            messages.error(request,'Not matched')
    return render(request,'new_password.html',message)

def about_me_view(request):
    return render(request,'aboutme.html')        
    
def follow_user(request, user_id):
    user_to_follow = Member.objects.get(id=user_id)
    Friendship.objects.get_or_create(from_user=request.user, to_user=user_to_follow)
    return redirect('details', id=user_to_follow.id)

def unfollow_user(request, user_id):
    user_to_unfollow = Member.objects.get(id=user_id)
    Friendship.objects.filter(from_user=request.user, to_user=user_to_unfollow).delete()
    return redirect('details', id=user_to_unfollow.id)
