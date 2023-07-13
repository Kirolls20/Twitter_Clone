from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from tweetLand.models import User



class User(AbstractUser):
    # profile_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    follows= models.ManyToManyField("self", related_name='followed_by',
            symmetrical=False,      
            blank=True)
    profile_pic = models.ImageField(null=True,blank=True,upload_to='images/')
    profile_background = models.ImageField(null=True,blank=True,upload_to='profile_bg/')
    date_created = models.DateField(auto_now_add=True)
    date_modified= models.DateTimeField(auto_now=True)




class Tweet(models.Model):
    user = models.ForeignKey(User,related_name='tweets' ,on_delete=models.DO_NOTHING)
    tweet = models.CharField(max_length=200,blank=False)
    tweet_pic = models.ImageField(null=True,blank=True,upload_to='images/tweets')
    likes = models.ManyToManyField(User,related_name='tweet_like',blank=True)
    comments= models.ManyToManyField(User,related_name='tweet_comment',through='Comment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def total_likes(self):
        return self.likes.count()

    def __str__(self):  
        return f'{self.user.username}  {self.created_at} '
    
    def total_comments(self):
        return self.comments.count()
    
class SavedTweet(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet,on_delete=models.CASCADE)
    saved_time= models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ['user','tweet']

    def __str__(self):
        return f'{self.user} {self.tweet.tweet}' 

class Comment(models.Model):
    comment = models.TextField()
    likes = models.ManyToManyField(User,related_name='comment_likes',blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




# def create_profile(sender,instance,created,**kwargs):
#     if created:
#         user_profile = User(user= instance)
#         # user_profile.save()
#         user_profile.follows.set([instance.User.id])
#         user_profile.save()
# post_save.connect(create_profile,sender=User)
