from typing import Any
from django import forms
from .models import Tweet,User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


class TweetForm(forms.ModelForm):
    tweet= forms.CharField(required=True,
        widget= forms.widgets.Textarea(
            attrs={
                'Placeholder':" Type Something...",
                'class': 'form-control',
            }
           
        ),
        label= ''

    )
    class Meta:
        model = Tweet
        exclude= ['user']

class SignupForm(UserCreationForm):
    first_name = forms.CharField( 
        required=True,
        max_length=120,
        widget= forms.widgets.TextInput(
                attrs={
                        'class':'form-control',
                        'placeholder': 'First Name'
                        }
                    ) ,
        label= ''
                                
            )
    last_name=forms.CharField( 
        required=True,
        max_length=120,
        widget= forms.widgets.TextInput(
                attrs={
                        'class':'form-control',
                        'placeholder': 'Last Name'
                        }
                    ) ,
        label= ''
                                
            )
    email = forms.EmailField(
        required=True,
        widget= forms.TextInput(
            attrs={
               'class':'form-control', 
               'placeholder':'Email Address'
            }
        
            ),
        label=''
        
    )
    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password1','password2')

    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] ='Username'
        self.fields['username'].label = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''





class UpdateUserProfileForm(forms.ModelForm):
    first_name = forms.CharField( 
        required=True,
        max_length=120,
        widget= forms.widgets.TextInput(
                attrs={
                        'class':'form-control',
                        'placeholder': 'First Name'
                        }
                    ) ,
        label= ''
                                
            )
    bio= forms.CharField(required=False,
        widget= forms.widgets.Textarea(
            attrs={
                'Placeholder':" Type Something...",
                'class': 'form-control',
            }
           
        ),
        label= ''

    )
    last_name=forms.CharField( 
        required=True,
        max_length=120,
        widget= forms.widgets.TextInput(
                attrs={
                        'class':'form-control',
                        'placeholder': 'Last Name'
                        }
                    ) ,
        label= ''
    
    )
    class Meta:
        model= User
        fields= ['username','first_name','last_name','bio','profile_pic']

    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label= ''