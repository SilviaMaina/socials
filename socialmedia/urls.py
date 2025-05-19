from django.urls import path, include
from .views import (
    index,
    create_post,
    get_post_detail,
    delete_post,
    create_comment,
    list_post_comments,
    get_comment_detail,
    delete_comment,
    like_post,
    unlike_post,
    like_comment,
    unlike_comment,
)

urlpatterns = [
    path('', index, name='index'),
    path('api/create_post/', create_post, name='create_post'),
    path('api/posts/<int:post_id>/', get_post_detail, name='get_post_detail'),
    path('api/posts/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('api/posts/<int:post_id>/comments/', list_post_comments, name='list_post_comments'),
    
    path('api/posts/<int:post_id>/create_comment/', create_comment, name='create_comment_for_post'),
    path('api/comments/<int:comment_id>/', get_comment_detail, name='get_comment_detail'),
    path('api/comments/<int:comment_id>/delete/', delete_comment, name='delete_comment'),

    path('api/posts/<int:post_id>/like/', like_post, name='like_post'),
    path('api/posts/<int:post_id>/unlike/', unlike_post, name='unlike_post'),
    path('api/comments/<int:comment_id>/like/', like_comment, name='like_comment'),
    path('api/comments/<int:comment_id>/unlike/', unlike_comment, name='unlike_comment'),
]