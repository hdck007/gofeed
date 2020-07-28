from django.contrib import admin
from .models import Post
from mptt.admin import MPTTModelAdmin

admin.site.register(Post)
