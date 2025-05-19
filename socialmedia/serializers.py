from rest_framework import serializers
from .models import Post, Comment, Like, LikeComment
from accounts.serializers import UserSerializer 


class PostSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)  
    pub_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)  
    post = serializers.PrimaryKeyRelatedField(read_only=True)  
    pub_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSerializer(read_only=True)
    date_liked = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Like
        fields = '__all__'

class LikeCommentSerializer(serializers.ModelSerializer):
    Comment = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSerializer(read_only=True)
    date_liked = serializers.DateTimeField(read_only=True)

    class Meta:
        model = LikeComment
        fields = '__all__'