
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from  PIL import Image



class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    image= models.ImageField(default='default.png',upload_to='profile_pics')
    contact=models.CharField(blank=True,max_length=50)
    
    
    def __str__(self):
        return f'{self.user.username}Profile'
    
    