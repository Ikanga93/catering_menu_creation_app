# menu_management/forms.py

from django import forms
from .models import Menu
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

'''
class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['title', 'description', 'image']  # Adjust fields based on your Menu model

# User creation
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))
    
    def clean_username(self):
        email = self.cleaned_data.get('username')
        try:
            user = User.objects.get(email=email)
            return user.username
        except User.DoesNotExist:
            raise ValidationError("Invalid email or password.")
'''
'''
Explanation:

UserRegistrationForm:

Inherits from UserCreationForm.
Adds an email field.
Overrides the clean_email method to ensure the email is unique.
UserLoginForm:

Inherits from AuthenticationForm.
Replaces the username field with an email field.
Overrides the clean_username method to authenticate using the email instead of the username.
'''