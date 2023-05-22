from django.urls import path
from . import views
from django.contrib.auth.views import LoginView  

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('user-list/',views.ListUSersView.as_view(),name='user_list'),
    path('profile/<int:pk>',views.ProfileView.as_view(),name='profile'),
    path('accounts/register/new-user/',views.RegisterView.as_view(),name='register'),
    path('accounts/login/',views.LoginView.as_view(),name='login'),
    path('accounts/logout/',views.LogoutView.as_view(),name='logout'),
    path('delete-tweet/<int:pk>/',views.DeleteTweetView.as_view(),name='delete_tweet'),
    path('edit-tweet/<int:pk>/',views.EditTweetView.as_view(),name='edit_tweet'),
]   