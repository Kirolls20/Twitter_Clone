from typing import Any, Dict
from django.urls import reverse,reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.http import HttpResponse 
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView,DeleteView,CreateView,UpdateView
from .models import Tweet,User,Comment,SavedTweet
from .forms import TweetForm,SignupForm,UpdateUserProfileForm,CommentForm
from django.urls import reverse_lazy 
# Class Based Views

class HomeView(ListView):
    model=Tweet
    context_object_name = 'tweets'
    template_name= 'home.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['tweets'] = Tweet.objects.all().order_by('-updated_at')
        context['form'] = TweetForm()
        return context
    

    def post(self,request):
        form = TweetForm(request.POST, request.FILES or None)
        if not request.user.is_authenticated:
            messages.warning(request, "Sorry, you are not logged in. Please sign in first and try again!")
            return redirect('home')  # Replace 'login' with your actual login URL
           
        if request.method =='POST':
            if form.is_valid():
                tweet=form.save(commit=False)
                tweet.user = self.request.user
                form.save()
                messages.success(request,('Tweet Sent!'))
                return redirect('home')

class DeleteTweetView(LoginRequiredMixin, TemplateView):
    template_name='home.html'       
    
    def post(self,request,**kwargs):
        tweet_id = self.kwargs['pk']
        obj = Tweet.objects.get(id= tweet_id)
        if request.method == 'POST':
            obj.delete()
            messages.success(request,('Tweet has been Deleted!!'))
            return redirect('home')
        else:
            return render(request,self.template_name)

class EditTweetView(LoginRequiredMixin,UpdateView):
    template_name= 'update_tweet.html'
    model= Tweet
    form_class =TweetForm
    success_url = reverse_lazy('home')
    
    # def get_context_data(self, **kwargs):
    #     context =  super().get_context_data(**kwargs)
    #     context['tweets'] = Tweet.objects.all().order_by('-updated_at')
    #     context['tweet_form'] = TweetForm()
    #     return context
    
    # def post(self,request,**kwargs):
    #     pass

class ListUSersView(LoginRequiredMixin,ListView):
    model= User
    context_object_name = 'users'
    template_name = 'user_list.html'

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['users'] =  User.objects.exclude(id=self.request.user.id)
        return context
    
class ProfileView(LoginRequiredMixin,DetailView):
    model = User
    context_object_name ='profile'
    template_name= 'profile.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['profile'] = User.objects.get(id=self.kwargs['pk'])
        context['tweets']  = Tweet.objects.filter(user=self.kwargs['pk']).order_by('-updated_at') ## HERE A PROBLEM ###
        return context

    # Follow and unfollow Function
    def post(self,request,pk):
        tweets = Tweet.objects.filter(user=self.kwargs['pk'])
        profile = User.objects.get(id=pk)
        if request.method == 'POST':
            current_user_profile = self.request.user
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)

        return render(request,  self.template_name , {'profile':profile,'tweets':tweets})


class CommentsView(LoginRequiredMixin,TemplateView):
    template_name= 'comment_list.html'
    
    def get_context_data(self, **kwargs) :
        context=  super().get_context_data(**kwargs)
        tweet_id = get_object_or_404(Tweet,id=self.kwargs['pk'])
        context['tweet_id'] = tweet_id
        context['total_comments'] = tweet_id.total_comments
        context['comments'] = Comment.objects.filter(tweet= tweet_id).order_by('-updated_at')
        context['comment_form'] = CommentForm()
        return context
    
    def post(self,request,pk):
        tweet_id = get_object_or_404(Tweet,id=pk)
        comment_form = CommentForm(request.POST)            
        if comment_form.is_valid():
            new_form = comment_form.save(commit=False)
            new_form.user = request.user
            new_form.tweet = tweet_id
            new_form.save()
            return redirect(reverse('comments_list', kwargs={'pk': pk}))
        else:
            messages.warning(request,('You Should Log in First !!'))
            return redirect('home')

class LikesView(LoginRequiredMixin,TemplateView):
    template_name= 'likes_page.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        tweet_id= get_object_or_404(Tweet,id=self.kwargs['pk'])
        like_list = tweet_id.likes.all()
        context['likes'] = like_list
        return context
    
def like_Tweet(request,pk , **kwargs):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet,id=pk)
        total_likes = Tweet.total_likes
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
            liked = False
        else:
            tweet.likes.add(request.user)
            liked = True
        
        # anchor= f"#tweet-{tweet.pk}"
        # url = reverse('home') + anchor
        # return(redirect(url))
        response_data = {
            'liked':liked,
            'total_likes' :total_likes
        }
        return JsonResponse(response_data)
    else:
        messages.warning(request,('You Should Log in First !!'))
        return redirect('home')
    


@login_required
def save_tweet(request,pk,**kwargs):
    tweet_id = get_object_or_404(Tweet,id=pk)
    if request.method == 'POST':
        if request.POST.get('save-tweet') == 'save':
            SavedTweet.objects.create(user=request.user,tweet=tweet_id)
            messages.success(request,('Tweet saved in your list! '))
    return redirect('home')

            
class RemoveFromSaved(LoginRequiredMixin, DeleteView):
    template_name = 'saved_tweets.html'
    model= SavedTweet
    success_url = reverse_lazy('saved_list')


# def comment_view(request,pk):
#     if request.user.is_authenticated:
#         tweet_id = get_object_or_404(Tweet,id=pk)
#         comment_form = CommentForm()
#         if request.method == 'POST':
#             if request.POST['comment']:
#                 comment_form = CommentForm(request.POST)
#                 if comment_form.is_valid():
#                     new_form = comment_form.save(commit=False)
#                     new_form.user = request.user
#                     new_form.tweet = tweet_id
#                     new_form.save()
#                     redirect('home')
#     else:
#         messages.warning(request,('You Should Log in First !!'))
#         return redirect('home')
#     return render(request,'comment_list.html',{'comment_form':comment_form})



class SavedList(LoginRequiredMixin,TemplateView):
    template_name = 'saved_tweets.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['saved_tweets'] = SavedTweet.objects.filter(user=self.request.user).all()
        return context


# User Classes and Functions

class RegisterView(CreateView):
    model=User
    form_class = SignupForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class LoginView(TemplateView):
    template_name='registration/login.html'

    def post(self,request):
        if request.method =='POST':
            username = request.POST['username']
            password = request.POST['password']
            user= authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,('You logged in Successfully!'))
                return redirect('home')
            else:
                messages.error(request,('Something went wrong try again!!'))
                return redirect('login')

class LogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,('You Loggedout See ya soon!'))
        return redirect('login')


class UpdateUserProfileView(LoginRequiredMixin,UpdateView):
    template_name = 'registration/update_user.html'
    model=User
    form_class= UpdateUserProfileForm

    def post(self,request,**kwargs):
        pk = self.kwargs['pk']
        current_user= User.objects.get(id=pk)
        if request.method == 'POST':
            form = UpdateUserProfileForm(request.POST ,request.FILES , instance = request.user)
            if form.is_valid():
                form.save()
                messages.success(request,('The Profile has been updated Successfully!'))
                return redirect('home')

