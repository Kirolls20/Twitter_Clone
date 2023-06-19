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
    path('accounts/update-profile/<int:pk>',views.UpdateUserProfileView.as_view(),name='update_profile'),
    path('delete-tweet/<int:pk>/',views.DeleteTweetView.as_view(),name='delete_tweet'),
    path('edit-tweet/<int:pk>/',views.EditTweetView.as_view(),name='edit_tweet'),
    path('like/<int:pk>',views.like_Tweet,name='like_tweet'),
    # path('comment/<int:pk>',views.comment_view,name='tweet_comment'),
    path('comment/list/<int:pk>',views.CommentsView.as_view(),name='comments_list'),
]   