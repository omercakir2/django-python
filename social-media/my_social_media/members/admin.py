from django.contrib import admin
from .models import Member,Friendship
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","email")
    list_display_links = ("first_name",)
    #list_editable = ("first_name",)
    

@admin.register(Friendship)    
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created_at')
    search_fields = ('from_user__username', 'to_user__username')

admin.site.register(Member,MemberAdmin)