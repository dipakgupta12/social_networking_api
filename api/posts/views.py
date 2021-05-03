from rest_framework import viewsets, generics, status
from .models import Post, User, UserPostActivity
from .serializers import PostSerializer, UserSerializer, UserPostActivitySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['post'], url_path="like_unlike")
    def like_unlike_post(self, request):
        activity_exists = UserPostActivity.objects.filter(
            user=request.user, post=request.data["post"]).exists()
        serializer = UserPostActivitySerializer(data=request.data)

        if activity_exists:
            instance = UserPostActivity.objects.get(
                user=request.user, post=request.data["post"])
            serializer = UserPostActivitySerializer(
                instance=instance, data=request.data)
        else:
            serializer.initial_data.update({"user": request.user.id})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
	serializer_class = UserSerializer
	queryset = User.objects.all()
