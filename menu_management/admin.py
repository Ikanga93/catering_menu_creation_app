from django.contrib import admin
from .models import Menu, Profile

admin.site.register(Menu)
admin.site.register(Profile)

'''
Usage:

Access Django Admin: Navigate to /admin/, log in with a superuser account, and manage menus and user profiles.
'''