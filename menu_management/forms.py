# menu_management/forms.py

from django import forms
from .models import Menu

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['title', 'description', 'image']  # Adjust fields based on your Menu model
