
from django.urls import path, include
from .views import PostViewset, UserViewSet
from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=True)
router.register('users', UserViewSet)
router.register('posts', PostViewset)
urlpatterns = router.urls
