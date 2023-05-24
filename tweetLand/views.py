from typing import Any, Dict
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.http import HttpResponse 
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView,DeleteView,CreateView,UpdateView
from .models import Tweet,User
from .forms import TweetForm,SignupForm,UpdateUserProfileForm
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
        form = TweetForm(request.POST or None)
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
        context['tweets']  = Tweet.objects.filter(id=self.kwargs['pk'])
        return context

    # Follow and unfollow Function
    def post(self,request,pk):
        profile = User.objects.get(id=pk)
        if request.method == 'POST':
            current_user_profile = self.request.user
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)

        return render(request,  self.template_name , {'profile':profile})



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
            form = UpdateUserProfileForm(request.POST or None , instance = request.user)
            if form.is_valid():
                form.save()
                messages.success(request,('The Profile has been updated Successfully!'))
                return redirect('home')
            
        
            

    

    


    

