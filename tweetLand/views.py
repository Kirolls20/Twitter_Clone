from typing import Any, Dict
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.http import HttpResponse 
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView
from .models import Profile,Tweet
from .forms import TweetForm
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
                return redirect('home')
        
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
                messages.success(request,('Something went wrong try again!!'))
                return redirect('login')

class LogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,('You Loggedout See ya soon!'))
        return redirect('login')


    
class ListUSersView(LoginRequiredMixin,ListView):
    model= Profile
    context_object_name = 'users'
    template_name = 'user_list.html'

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['users'] =  Profile.objects.exclude(user=self.request.user)
        return context
    
class ProfileView(LoginRequiredMixin,DetailView):
    model = Profile
    context_object_name ='profile'
    template_name= 'profile.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(id=self.kwargs['pk'])
        context['tweets']  = Tweet.objects.filter(user_id=self.kwargs['pk'])
        return context

    # Follow and unfollow Function
    def post(self,request,pk):
        profile = Profile.objects.get(user_id=pk)
        if request.method == 'POST':
            current_user_profile = self.request.user.profile
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)

        return render(request,  self.template_name , {'profile':profile})


    

