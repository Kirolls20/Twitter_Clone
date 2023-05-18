from django import forms
from .models import Tweet

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
