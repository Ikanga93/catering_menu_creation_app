# menu_management/serializers.py

from rest_framework import serializers
from .models import Menu
from django.contrib.auth.models import User

# MenuSerializer
class MenuSerializer(serializers.ModelSerializer):
    caterer = serializers.ReadOnlyField(source='caterer.username')  # Display username instead of ID
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Menu
        fields = ['id', 'title', 'description', 'image', 'caterer', 'created_at', 'updated_at']

# UserRegistrationSerializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        
         # Ensure email is unique
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email is already in use."})
        
        return data

    def create(self, validated_data):
        # Remove password2 as it's not needed for user creation
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')  # Include other fields as necessary


'''
Explanation:
MenuSerializer: Serializes the Menu model.
UserRegistrationSerializer: Handles user registration with password confirmation.
UserSerializer: Serializes the User model, which is needed in your views.py.
'''