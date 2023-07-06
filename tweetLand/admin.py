from django.contrib import admin
from django.contrib.auth.models import Group,User
from .models import Tweet,User,Comment,SavedTweet

# Register and UnRegister your models here.
admin.site.unregister(Group)
admin.site.register(User)
# admin.site.register(Profile)
admin.site.register(Tweet)
admin.site.register(Comment)
admin.site.register(SavedTweet)

# Expand The User model with profile model inline 
# class UserProfileInline(admin.StackedInline):
#     model= Profile

# # Extend User Admin Model
# class UserAdmin(admin.ModelAdmin):
#     model= User
#     fields = ['username']
#     # inlines = [UserProfileInline]

# UnRegister Old User Admin

# Register My Custom User Admin 
# admin.site.register(User,UserAdmin)