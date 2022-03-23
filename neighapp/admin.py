from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Profile)
admin.site.register(Business)
admin.site.register(Category)
admin.site.register(Neighbourhood)
admin.site.register(Contact)
admin.site.register(Post)
admin.site.register(Location)
