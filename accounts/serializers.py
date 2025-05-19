from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Follower

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def create(self, validate_data):
        user = User.objects.create_user(
            username=validate_data['username'],
            email=validate_data['email'],
            password=validate_data['password']
        )
        
        return user

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']   
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']    

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.user.following.count()  

class FollowerSerializer(serializers.ModelSerializer):
    follower_id = serializers.ReadOnlyField(source='follower.id')
    followed_id = serializers.ReadOnlyField(source='followed.id')
    
    class Meta:
        model = Follower
        fields = ['id', 'follower_id', 'followed_id', 'created_at']