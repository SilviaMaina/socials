from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, LikeCommentSerializer
from .models import Post, Comment, Like, LikeComment

def index(request):
    return HttpResponse('My app is running!')


@swagger_auto_schema(
    method='POST', 
    request_body=PostSerializer,
    responses = {
        201: "User Created",
        400: 'Bad Request',
        401: 'Unauthorized',
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create_post(request):
    if request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['writer'] = request.user
            serializer.save()
            return Response({
            "message": "Post created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='GET',
    responses = {
        200: PostSerializer,
        404: "Not Found",
        401: 'Unauthorized',
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def get_post_detail(request, post_id):
    """
    Retrieve a single post by its ID.
    """
    post = get_object_or_404(Post, pk=post_id)
    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='GET',
    responses = {
        200: CommentSerializer(many=True),
        404: "Post Not Found",
        401: 'Unauthorized',
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def list_post_comments(request, post_id):
    """
    Retrieve all comments for a specific post.
    """
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
        method='PATCH',
        request_body=PostSerializer,
        responses = {
            200: PostSerializer,
            400: 'Bad Request',
            401: 'Unauthorized',
            404: 'Post Not Found'
        }
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_post(request, post_id):
    """
    Update a post by its ID. Only the author can update their post.
    """
    post = get_object_or_404(Post, pk=post_id)  
    serializer = PostSerializer(post, data=request.data, partial=True)

    if serializer.is_valid():
        if serializer.validated_data.get('writer') != request.user:
            return Response({"detail": "You do not have permission to update this post."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer.save()
            return Response({
            "message": "Post updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        "message": "Post update failed",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)        

@swagger_auto_schema(
    method='DELETE',
    request_body=no_body, # Indicate that the delete request does not have a body
    responses = {
        204: "No Content", # Standard response for successful deletion
        403: "Permission Denied", # User is not the author
        404: "Not Found",
        401: 'Unauthorized',
    }
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    """
    Delete a post by its ID. Only the author can delete their post.
    """
    post = get_object_or_404(Post, pk=post_id)

    # Check if the authenticated user is the writer of the post
    if post.writer != request.user:
        return Response({"detail": "You do not have permission to delete this post."},
                        status=status.HTTP_403_FORBIDDEN)

    post.delete()
    # 204 No Content is a standard response for successful DELETE requests
    return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='GET',
    responses = {
        200: CommentSerializer,
        404: "Not Found",
        401: 'Unauthorized',
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comment_detail(request, comment_id):
    """
    Retrieve a single comment by its ID.
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='POST', 
    request_body=CommentSerializer,
    responses = {
        201: "User Created",
        400: 'Bad Request',
        401: 'Unauthorized',
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['writer'] = request.user
            serializer.validated_data['post'] = post
            serializer.save()
            return Response({
            "message": "Comment created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response({
        "message": "comment creation failed",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
    method='DELETE',
    request_body=no_body,
    responses = {
        204: "No Content", 
        403: "Permission Denied", 
        404: "Not Found",
        401: 'Unauthorized',
    }
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    """
    Delete a comment by its ID. Only the author can delete their comment.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    # Ensure only the comment's author can delete it
    if not comment.writer == request.user:
        return Response({"detail": "You are not allowed to delete this comment."}, status=status.HTTP_403_FORBIDDEN)
    
    comment.delete()
    # 204 No Content is a standard response for successful DELETE requests
    return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='PATCH',
    request_body=CommentSerializer,
    responses = {
        200: CommentSerializer,
        400: 'Bad Request',
        401: 'Unauthorized',
        404: 'Comment Not Found'
    }
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    """
    Update a comment by its ID. Only the author can update their comment.
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    serializer = CommentSerializer(comment, data=request.data, partial=True)

    if serializer.is_valid():
        if serializer.validated_data.get('writer') != request.user:
            return Response({"detail": "You do not have permission to update this comment."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer.save()
            return Response({
            "message": "Comment updated successfully",
            "data": serializer.data
            }, status=status.HTTP_200_OK)
    
    return Response({
        "message": "Comment update failed",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method = "POST",
    request_body = LikeSerializer,
    responses = {
        201: "Like Created",
        400: 'Bad Request',
        401: 'Unauthorized',
        404: 'Post Not Found'
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    """
    Like a post by its ID.
    """
    post = get_object_or_404(Post, pk=post_id)
    serializer = LikeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['user'] = request.user
        serializer.validated_data['post'] = post
        serializer.save()
        return Response({
            "message": "Post liked successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        "message": "Like creation failed",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method = "DELETE",
    request_body = no_body,
    responses = {
        204: "No Content",
        400: 'Bad Request',
        401: 'Unauthorized',
        404: 'Post Not Found'
    })
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike_post(request, post_id):
    """
    Unlike a post by its ID.
    """
    post = get_object_or_404(Post, pk=post_id)  
    like = get_object_or_404(Like, user=request.user, post=post)
    like.delete()
    return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@swagger_auto_schema(
    method = "POST",
    request_body = LikeCommentSerializer,
    responses = {
        201: "Like Created",
        400: 'Bad Request',
        401: 'Unauthorized',
        404: 'Post Not Found'
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request, comment_id):
    """
    Like a comment by its ID.
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    serializer = LikeCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['user'] = request.user
        serializer.validated_data['comment'] = comment
        serializer.save()
        return Response({
            "message": "comment liked successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        "message": "Like creation failed",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method = "DELETE",
    request_body = no_body,
    responses = {
        204: "No Content",
        400: 'Bad Request',
        401: 'Unauthorized',
        404: 'Post Not Found'
    })
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike_comment(request, comment_id):
    """
    Unlike a comment by its ID.
    """
    comment = get_object_or_404(Comment, pk=comment_id)  
    like = get_object_or_404(Like, user=request.user, comment=comment)
    like.delete()
    return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)