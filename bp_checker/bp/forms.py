# Import django forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, History
from django.core.exceptions import ValidationError
from numpy import random
from threading import Timer



class RegistrationForm(UserCreationForm):
    
    CHOICES = [('', 'Gender'),('Male', 'Male'), ('Female', 'Female')]
    
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Create Your username',
        }), label=False)
    
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter first name',
        }), label=False)
    
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter last name',   
            'type': 'text'   
        }), label=False)
    
    email = forms.EmailField(
        widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter email',   
            'type': 'email'  
        }), label=False)
    
    phone_no = forms.CharField(max_length=11,
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone',
        }), label=False)
    
    gender = forms.ChoiceField(widget=forms.Select(attrs={
            'class': 'form-control'
        }), choices=CHOICES, label=False)
    
    password1 = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Create password',
            'type': 'password'
        }), label=False, min_length=6)
    
    password2 = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'type': 'password'
        }), label=False,  min_length=6)
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email","phone_no", "gender", "password1", "password2"]

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Username'}
    ), label=False)
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder':'Password'}
    ), label=False)

   

class BpForm(forms.Form):  
      
    education = [('', 'Education'),('1', 'Primary'), ('2', 'Secondary'),  ('3', 'Graduate'), ('4', 'Master')]
    smoke = [('', 'Current smoker'),('2', 'Yes'), ('1', 'No')]
    
    education = forms.ChoiceField(widget=forms.Select(attrs={
            'class': 'form-control'
        }), choices=education)  
   
    age = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Age in years',  
            'type': 'number'
        }))
    
    bmi = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Body mass index',     
            'type': 'number'
        }))
    
    c_smoker = forms.ChoiceField(widget=forms.Select(attrs={
            'class': 'form-control'
        }), choices=smoke)
    
    heart_rate = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Heart rate',  
            'type': 'number'
        }))
    
    
    class Meta:
        model = History
        
        
    # def clean(self):
    #     cleaned_data = super().clean()
    #     age = self.cleaned_data.get("age")
    #     print(age)
    #     return self.age

    
    
    
class UserUpdate(forms.Form):
    phone_no = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Enter new Phone number',
        'type': 'number'
    }), label=False, min_length=11)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     phone_no = cleaned_data.get("phone_no")
    #     print(phone_no)
    #     if phone_no.isdigit() == False:
    #         raise ValidationError("Invalid phone number")
    #     return phone_no

    
    class Meta:
         model = UserProfile
         fields = ['phone_no'] 
         widgets = {
             'phone_no':forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter new Phone number','type': 'number', 'label': 'False'} )
            }
         
         
    