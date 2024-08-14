from django.contrib import admin
from .models import Member
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ("firstname","lastname","phone","join_date","email")

admin.site.register(Member,MemberAdmin)