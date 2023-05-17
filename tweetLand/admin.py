from django.contrib import admin
from django.contrib.auth.models import Group,User
from .models import Profile ,Tweet

# Register and UnRegister your models here.
admin.site.unregister(Group)
admin.site.register(Profile)
admin.site.register(Tweet)

# Expand The User model with profile model inline 
class UserProfileInline(admin.StackedInline):
    model= Profile

# Extend User Admin Model
class UserAdmin(admin.ModelAdmin):
    model= User
    fields = ['username']
    # inlines = [UserProfileInline]

# UnRegister Old User Admin
admin.site.unregister(User)

# Register My Custom User Admin 
admin.site.register(User,UserAdmin)