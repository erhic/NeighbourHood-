from os import name
from django.shortcuts import render,redirect

# Create your views here.
# from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm

from django.contrib.auth.decorators import login_required
# from .models import Profile
from .models import *


def home(request):
    return render(request,'neighapp/base.html')


def register(request):
    
    if request.method == 'POST':
        # if form as method post and there is data posted return
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('profileacc')
    else:
        
        form=UserRegisterForm()
    
    context={'form':form}
    return render(request, 'neighapp/register.html',context)

@login_required
def profileacc(request):
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        
        if  u_form.is_valid()and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated')
            return redirect('index')
    
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user)
        
        
    
    context={
        'u_form':u_form,
        'p_form':p_form
        
    }
    return render(request,'neighapp/profile.html',context)





#
@login_required
def index(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    if profile is None:
        profile = Profile.objects.filter(
            user_id=current_user.id).first()  
        posts = Post.objects.filter(user_id=current_user.id)
        locations = Location.objects.all()
        neighbourhood = Neighbourhood.objects.all()
        category = Category.objects.all()
        business = Business.objects.filter(user_id=current_user.id)
        contacts = Contact.objects.filter(user_id=current_user.id)
        return render(request, "neighapp/mainprofile.html", {"danger": "Update Profile ", "locations": locations, "neighbourhood": neighbourhood, "categories": category, "business": business, "contacts": contacts, "posts": posts})
    else:
        neighbourhood = profile.neighbourhood
        posts = Post.objects.filter(neighbourhood=neighbourhood).order_by("-created_at")
        return render(request, 'neighapp/index.html', {'posts': posts})


@login_required
def profile(request):
    current_user = request.user
    profile = Profile.objects.filter(
        user_id=current_user.id).first()  
    posts = Post.objects.filter(user_id=current_user.id)
    locations = Location.objects.all()
    neighbourhood = Neighbourhood.objects.all()
    category = Category.objects.all()
    business = Business.objects.filter(user_id=current_user.id)
    contacts = Contact.objects.filter(user_id=current_user.id)
    return render(request, 'neighapp/mainprofile.html', {'profile': profile, 'posts': posts, 'locations': locations, 'neighbourhood': neighbourhood, 'categories': category, 'business': business, 'contacts': contacts})



@login_required
def update_profile(request):
    if request.method == "POST":

        current_user = request.user

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        name = request.POST["first_name"] + " " + request.POST["last_name"]

        neighbourhood = request.POST["neighbourhood"]
        location = request.POST["location"]

        
        if location == "":
            location = None
        else:
            location = Location.objects.get(name=location)

        #
        if neighbourhood == "":
            neighbourhood = None
        else:
            neighbourhood = Neighbourhood.objects.get(name=neighbourhood)

        profile_image = request.FILES["profile_pic"]
        profile_image = cloudinary.uploader.upload(profile_image)
        profile_url = profile_image["url"]

        user = User.objects.get(id=current_user.id)

        
        if Profile.objects.filter(user_id=current_user.id).exists():

            profile = Profile.objects.get(user_id=current_user.id)
            profile.profile_pic = profile_url
            profile.neighbourhood = neighbourhood
            profile.location = location
            profile.save()
        else:
            profile = Profile(
                user_id=current_user.id,
                name=name,
                profile_pic=profile_url,
                neighbourhood=neighbourhood,
                location=location,
            )

            profile.save_profile()

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        user.save()

        return redirect("/profile", {"success": "Profile Updated Successfully"})

    else:
        return render(request, "neighapp/profile.html", {"danger": "Update Failed"})


@login_required
def create_post(request):
    if request.method == "POST":
        current_user = request.user
        title = request.POST["title"]
        content = request.POST["content"]
        category = request.POST["category"]
        location = request.POST["location"]
        

      
        profile = Profile.objects.filter(user_id=current_user.id).first()
       
        if profile is None:
            profile = Profile.objects.filter(
                user_id=current_user.id).first()  
            posts = Post.objects.filter(user_id=current_user.id)
            
            locations = Location.objects.all()
            neighbourhood = Neighbourhood.objects.all()
            category = Category.objects.all()
            business = Business.objects.filter(user_id=current_user.id)
            contacts = Contact.objects.filter(user_id=current_user.id)
           
            return render(request, "neighapp/profile.html", {"danger": "Update Profile", "locations": locations, "neighbourhood": neighbourhood, "categories": category, "business": business, "contacts": contacts, "posts": posts})
        else:
            neighbourhood = profile.neighbourhood

       
        if category == "":
            category = None
        else:
            category = Category.objects.get(name=category)

        
        if location == "":
            location = None
        else:
            location = Location.objects.get(name=location)

  
        if request.FILES:
            image = request.FILES["image"]
            #
            image = cloudinary.uploader.upload(
                image, crop="limit", width=800, height=600)
           
            image_url = image["url"]

            post = Post(
                user_id=current_user.id,
                title=title,
                content=content,
                category=category,
                location=location,
                image=image_url,
                
                neighbourhood=neighbourhood,
            )
            post.create_post()

            return redirect("/profile", {"success": "Post Created Successfully"})
        else:
            post = Post(
                user_id=current_user.id,
                title=title,
                content=content,
                category=category,
                location=location,
                neighbourhood=neighbourhood,
            )
            post.create_post()

            return redirect("/profile", {"success": "Post Created Successfully"})

    else:
        return render(request, "profile.html", {"danger": "Post Creation Failed"})


# create business
@login_required
def create_business(request):
    if request.method == "POST":
        current_user = request.user
        name = request.POST["name"]
        email = request.POST["email"]
        profile = Profile.objects.filter(user_id=current_user.id).first()
        if profile is None:
            profile = Profile.objects.filter(
                user_id=current_user.id).first() 
            posts = Post.objects.filter(user_id=current_user.id)
            locations = Location.objects.all()
            neighbourhood = Neighbourhood.objects.all()
            category = Category.objects.all()
            business = Business.objects.filter(user_id=current_user.id)
            contacts = Contact.objects.filter(user_id=current_user.id)
            return render(request, "neighapp/profile.html", {"danger": "Update Profile", "locations": locations, "neighbourhood": neighbourhood, "categories": category, "business": business, "contacts": contacts, "posts": posts})
        else:
            neighbourhood = profile.neighbourhood
        if neighbourhood == "":
            neighbourhood = None
        else:
            neighbourhood = Neighbourhood.objects.get(name=neighbourhood)
        business = Business(
            user_id=current_user.id,
            name=name,
            email=email,
            neighbourhood=neighbourhood,
        )
        business.create_business()

        return redirect("/profile", {"success": "Business Created Successfully"})
    else:
        return render(request, "neighapp/profile.html", {"danger": "Failed"})



@login_required
def create_contact(request):
    if request.method == "POST":
        current_user = request.user
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        profile = Profile.objects.filter(user_id=current_user.id).first()
        if profile is None:
            profile = Profile.objects.filter(
                user_id=current_user.id).first()  
            posts = Post.objects.filter(user_id=current_user.id)
            locations = Location.objects.all()
            neighbourhood = Neighbourhood.objects.all()
            category = Category.objects.all()
            business = Business.objects.filter(user_id=current_user.id)
            contacts = Contact.objects.filter(user_id=current_user.id)
            return render(request, "neighapp/profile.html", {"danger": "Update Profile ", "locations": locations, "neighbourhood": neighbourhood, "categories": category, "business": business, "contacts": contacts, "posts": posts})
        else:
            neighbourhood = profile.neighbourhood
        if neighbourhood == "":
            neighbourhood = None
        else:
            neighbourhood = Neighbourhood.objects.get(name=neighbourhood)

        contact = Contact(
            user_id=current_user.id,
            name=name,
            email=email,
            phone=phone,
            neighbourhood=neighbourhood,
        )
        contact.create_contact()

        return redirect("/profile", {"success": "Contact Created Successfully"})
    else:
        return render(request, "neighapp/profile.html", {"danger": "Contact Creation Failed"})




@login_required
def get_business(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    if profile is None:
        profile = Profile.objects.filter(
            user_id=current_user.id).first()  
        posts = Post.objects.filter(user_id=current_user.id)
        locations = Location.objects.all()
        business = Business.objects.filter(user_id=current_user.id)
        contacts = Contact.objects.filter(user_id=current_user.id)
        neighbourhood = Neighbourhood.objects.all()
        category = Category.objects.all()
    
        return render(request, "neighapp/profile.html", {"danger": "Update Profile ", "locations": locations, "neighbourhood": neighbourhood, "categories": category, "business": business, "contacts": contacts, "posts": posts})
    else:
        neighbourhood = profile.neighbourhood
        business = Business.objects.filter(
            neighbourhood=profile.neighbourhood)
        return render(request, "neighapp/business.html", {"business": business})


@login_required
def get_contact(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    if profile is None:
        profile = Profile.objects.filter(
            user_id=current_user.id).first() 
        posts = Post.objects.filter(user_id=current_user.id)
        locations = Location.objects.all()
        business = Business.objects.filter(user_id=current_user.id)
        contacts = Contact.objects.filter(user_id=current_user.id)
        neighbourhood = Neighbourhood.objects.all()
        category = Category.objects.all()
        
        return render(request, "neighapp/profile.html", {"danger": "Update Profile ", "locations": locations, "neighbourhood": neighbourhood, "categories": category, "business": business, "contacts": contacts, "posts": posts})
    else:
        neighbourhood = profile.neighbourhood
        contacts = Contact.objects.filter(neighbourhood=profile.neighbourhood).order_by("-created_at")
        return render(request, "neighapp/contacts.html", {"contacts": contacts, "neighbourhood": profile.neighbourhood})



@login_required
def search(request):
    if 'search_term' in request.GET and request.GET["search_term"]:
        search_term = request.GET.get("search_term")
        searched_business = Business.objects.filter(name__icontains=search_term)
        message = f"Search For: {search_term}"

        return render(request, "neighapp/search.html", {"message": message, "business": searched_business})
    else:
        message = "You haven't searched for any term"
        return render(request, "neighapp/search.html", {"message": message})

