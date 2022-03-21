
from tkinter import CASCADE
from unicodedata import name
from venv import create
from django.db import models
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import User
from  PIL import Image



class Profile(models.Model):
    '''
    This a model for ;database table with field of every profile for  each created user in the application.
    '''
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
            
class Location(models.Model):
    '''
    This a model for ;database table for location, a generic table to used as by other models to attach location .
    '''
    name=models.CharField(max_length=50,min_length=3)
    
    def __str__(self):
        return name
    
class Neighbourhood(models.Model):
    '''
    This a model for ;database table for neighbourhood, every user has to be from a certian neighbourhood,evry business,post is attached to a neighbourhood.
    '''
    name=models.CharField(max_length=50,min_length=3)
    location=models.ForeignKey(Location,on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    population = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save_neigborhood(self):
        self.save()

    @classmethod
    def delete_neighbourhood(cls, id):
        cls.objects.filter(id=id).delete()

    @classmethod
    def update_neighbourhood(cls, id):
        cls.objects.filter(id=id).update()

    @classmethod
    def search_by_name(cls, search_term):
        hood = cls.objects.filter(name__icontains=search_term)
        return hood

    @classmethod
    def find_neigborhood(cls, id):
        hood = cls.objects.get(id=id)
        return hood
    
    def __str__(self):
        return name
