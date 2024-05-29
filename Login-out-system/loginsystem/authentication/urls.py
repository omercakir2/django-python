from django.contrib import admin
from django.urls import path, include
from . import views
from .views import VerifyEmail




urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('profile',views.profile,name="profile"),
    path('verify-email/<int:user_id>/<uuid:verification_code>/', VerifyEmail.as_view(), name='verify_email'),
]
