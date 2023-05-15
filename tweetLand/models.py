from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create Tweet Model 
class Tweet(models.Model):
    user= models.ForeignKey(User,related_name='tweets' ,on_delete=models.DO_NOTHING)
    tweet = models.CharField(max_length=200,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

# Create your models here.
class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    follows= models.ManyToManyField("self", related_name='followed_by',
            symmetrical=False,
            blank=True)
    date_created = models.DateField(User,auto_now_add=True)
    date_modified= models.DateTimeField(User,auto_now=True)
    
    
    def __str__(self):
        return self.user.username
    

def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile = Profile(user= instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
post_save.connect(create_profile,sender=User)
