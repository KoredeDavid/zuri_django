from django.contrib import admin
from .models import  Category, Post, Comment, CustomUser

# Register your models here.

# admin.site.register(Project)

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CustomUser)
