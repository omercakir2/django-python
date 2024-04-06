from django.db import models

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
# Create your models here.
# Doing our jobs related to databases
  
#>>>Member.objects.all().values() to look data
#>>> member = Member(firstname='Emil', lastname='Refsnes')
#>>> member.save()
  
# '>>>' means you are workin in a python shell (execute this 'python3 manage.py shell')