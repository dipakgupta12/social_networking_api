from rest_framework import serializers
from .models import Post, UserPostActivity, UserLocationDetail
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from .user_holidays import is_today_holiday_in_user_country
from .tasks import save_user_ip_location_holiday


class PostSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ("id", "title", "description", "created_by",)


class UserLocationDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserLocationDetail
        exclude = ("id", "user")


class UserPostActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPostActivity
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    location = UserLocationDetailSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name",
                  "email", "password", "username", "location"]

    def validate_password(self, password):
        return make_password(password)

    def validate_email(self, email):
        validate_email(email)
        return email

    def create(self, validated_data):
        request = self.context["request"]
        user = User.objects.create(**validated_data)

        # Shared task
        save_user_ip_location_holiday.delay(request.geolocation, user.id)
        return user
