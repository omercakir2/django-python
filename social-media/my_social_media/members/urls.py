from django.urls import path
from . import views
from .views import register_view, login_view, logout_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home,name='home'),
    path('members/', views.members, name='members'),
    path('members/details/<int:id>',views.details,name='details'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('success/',views.success_view , name='success'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/forget-password',views.forget_password_view,name='forget_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password_view, name='reset_password'),
    path('members/details/<int:id>/edit',views.edit_view,name='edit'),
    path('creator/',views.about_me_view,name='about_me'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)