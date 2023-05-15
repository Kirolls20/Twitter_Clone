from typing import Any, Dict
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse 
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView
from .models import Profile
# Class Based Views

class HomeView(TemplateView):
    template_name= 'home.html'


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



    

