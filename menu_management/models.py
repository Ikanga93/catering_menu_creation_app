# menu_management/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Menu(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    caterer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='menus')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class Profile(models.Model):
    USER_ROLES = (
        ('caterer', 'Caterer'),
        ('customer', 'Customer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='customer')

    def __str__(self):
        return f"{self.user.username} Profile"


'''
Explanation:

title: Name of the menu.
description: Detailed description.
image: Optional image representing the menu.
caterer: Foreign key linking to the User who created the menu.
created_at & updated_at: Timestamps for tracking.
'''