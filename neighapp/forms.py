from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 

from .models import Profile

# a below created a class userregistration form and inherited UserCreationForm to overide it by adding fields and styling it#
class UserRegisterForm(UserCreationForm):
    
    email=forms.EmailField()
    
    class Meta:
        
        model=User
        fields=['username','email','password1','password2']
 
 
# forms below will rely on model which inthis case is profile   
# form below will rely on model which inthis case is profile   
class UserUpdateForm(forms.ModelForm):
    
    email=forms.EmailField()
    
    class Meta:
        
        model=User
        fields=['username','email']
    

    


class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        
        model=Profile
        fields=['image','contact']

    