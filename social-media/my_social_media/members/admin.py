from django.contrib import admin
from .models import Member
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","email")
    list_display_links = ("first_name",)
    #list_editable = ("first_name",)
    

admin.site.register(Member,MemberAdmin)