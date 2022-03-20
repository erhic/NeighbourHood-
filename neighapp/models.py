
from venv import create
from django.db import models
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import User
from  PIL import Image



class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    image= models.ImageField(default='default.png',upload_to='profile_pics')
    contact=models.CharField(blank=True,max_length=50)
    location=models.CharField(blank=True,max_length=50)
    bio=models.CharField(blank=True,max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.user.username}Profile'
    
    def save(self,**kwarg):
        super().save()
        #  the below variable will store  every instance of the image before risizing
        img= Image.open(self.image.path)
        
        if img.height>300 or img.width>300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        