
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
    name=models.CharField(max_length=50,min_length=3)
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    image= models.ImageField(default='default.png',upload_to='profile_pics')
    contact=models.CharField(blank=True,max_length=50)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey('NeighbourHood', on_delete=models.CASCADE)
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

class Business(models.Model):
    '''
    This a model for ;database table for business, a user can have a  business and every business is to be in a certain neighbourhood.
    '''
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey('NeighbourHood', on_delete=models.CASCADE)
    bs_email = models.EmailField(max_length=20)
    bs_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    def update_business(self):
        self.update()

    @classmethod
    def search_by_name(cls, search_term):
        business = cls.objects.filter(name__icontains=search_term)
        return business

    @classmethod
    def find_business(cls, id):
        business = cls.objects.get(id=id)
        return business

    def __str__(self):
        return self.name
    
class Post(models.Model):
    '''
    This a model for ;database table for post, a user can make a which will be of certain business, category and from certain neighbourhood.
    '''
    topic = models.CharField(max_length=70)
    content = models.TextField(blank=True, null=True)
    post_image= models.ImageField(default='default.png',upload_to='post_pics')
    
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey('NeighbourHood', on_delete=models.CASCADE, default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()

    def update_post(self):
        self.update()

    @classmethod
    def search_by_title(cls, search_term):
        post = cls.objects.filter(title__icontains=search_term)
        return post

    @classmethod
    def find_post(cls, id):
        post = cls.objects.get(id=id)
        return post

    def __str__(self):
        return self.title
 
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    neighbourhood = models.ForeignKey('NeighbourHood', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save_contact(self):
        self.save()

    def delete_contact(self):
        self.delete()

    def update_contact(self):
        self.update()

    @classmethod
    def search_by_name(cls, search_term):
        contact = cls.objects.filter(name__icontains=search_term)
        return contact
    
    @classmethod
    def find_contact(cls, id):
        contact = cls.objects.get(id=id)
        return contact

    def __str__(self):
        return self.name