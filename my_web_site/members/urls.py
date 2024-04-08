from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'), 
    # this part is for indicating the url
    #that we use to access the app
]