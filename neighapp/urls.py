from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from neighapp import views as user_views
from neighapp import views 

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('home/', views.home, name='home'),
    path('profileacc/',views.profile, name='profileacc'),
   
#    using  LoginView and LogoutView, class based views, they have the logic but we show them how to handle templates
    path('login',auth_views.LoginView.as_view(template_name='neighapp/login.html'),name='login'),
    path('logout',auth_views.LogoutView.as_view(template_name='neighapp/logout.html'),name='logout')
    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
