from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.db.models import fields
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = models.EmailField()

    class Meta:
        model = User
        fields = ['username' , 'email' , 'password1' , 'password2']
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username' , 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio' , 'phone' , 'image']


#users


class UserSearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100)

class SignUpForm(UserCreationForm):
    biography = forms.CharField(max_length=500, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'biography', 'profile_picture')

    def save(self, commit=True):
        user = super().save(commit=False)
        user_profile = Profile.objects.create(user=user, biography=self.cleaned_data['biography'], profile_picture=self.cleaned_data['profile_picture'])
        if commit:
            user.save()
            user_profile.save()
        return user