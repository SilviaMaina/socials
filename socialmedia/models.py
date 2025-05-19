from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    pub_date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    images = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.writer} - {self.pub_date}"
    

class Comment(models.Model):
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.content} - {self.writer} - {self.post}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    is_liked = models.BooleanField(default=False)
    date_liked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post} - {self.user}"

class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='like_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_comments')
    is_liked = models.BooleanField(default=False)
    date_liked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment} - {self.user}"