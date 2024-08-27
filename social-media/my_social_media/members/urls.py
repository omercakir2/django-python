from django.urls import path
from . import views
from .views import register_view, login_view, logout_view

urlpatterns = [
    path('',views.home,name='home'),
    path('members/', views.members, name='members'),
    path('members/details/<int:id>',views.details,name='details'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('success/',views.success_view , name='success'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    
]