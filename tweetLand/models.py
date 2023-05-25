from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from tweetLand.models import User

# Create Tweet Model 

class User(AbstractUser):
    # profile_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    follows= models.ManyToManyField("self", related_name='followed_by',
            symmetrical=False,      
            blank=True)
    profile_pic = models.ImageField(null=True,blank=True,upload_to='images/')
    date_created = models.DateField(auto_now_add=True)
    date_modified= models.DateTimeField(auto_now=True)
    


class Tweet(models.Model):
    user = models.ForeignKey(User,related_name='tweets' ,on_delete=models.DO_NOTHING)
    tweet = models.CharField(max_length=200,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}  {self.created_at} '


# # Create your models here.
# class Profile(models.Model):
#     
    
    
    # def __str__(self):
    #     return self.user.username
    

# def create_profile(sender,instance,created,**kwargs):
#     if created:
#         user_profile = User(user= instance)
#         # user_profile.save()
#         user_profile.follows.set([instance.User.id])
#         user_profile.save()
# post_save.connect(create_profile,sender=User)
