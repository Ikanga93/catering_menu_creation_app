# menu_management/serializers.py

from rest_framework import serializers
from .models import Menu
from django.contrib.auth.models import User

# MenuSerializer
class MenuSerializer(serializers.ModelSerializer):
    caterer = serializers.ReadOnlyField(source='caterer.username')  # Display username instead of ID

    class Meta:
        model = Menu
        fields = ['id', 'title', 'description', 'image', 'caterer', 'created_at', 'updated_at']

# UserRegistrationSerializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
