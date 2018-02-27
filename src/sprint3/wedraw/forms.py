from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from wedraw.models import *
from django import forms


class SignUpForm(forms.Form):
    password1 = forms.CharField(max_length = 200, 
                                widget = forms.PasswordInput(attrs = {'placeholder': 'Password','class' : 'form-control'}))
    password2 = forms.CharField(max_length = 200,
                                widget = forms.PasswordInput(attrs = {'placeholder': 'Confirm Password','class' : 'form-control'}))
    username = forms.CharField(max_length = 20)
    def clean(self):
        cleaned_data = super(SignUpForm,self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password did not match")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.    
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact = username):
            raise forms.ValidationError("User name is already taken")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class GuessingForm(forms.Form):
    guess = forms.CharField(max_length = 30)
    def clean(self):
        cleaned_data = super(GuessingForm, self).clean()
        # Generally return the cleaned data we got from our parent.
        return cleaned_data

