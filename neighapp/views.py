from django.shortcuts import render,redirect

# Create your views here.
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm

from django.contrib.auth.decorators import login_required


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
            return redirect('home')
    else:
        
        # else return a clean or empty form
        form=UserRegisterForm()
    
    context={'form':form}
    return render(request, 'neighapp/register.html',context)
