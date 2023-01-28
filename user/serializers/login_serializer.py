from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    user_id = serializers.CharField(max_length=255, read_only=True)
    error = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        if email is None:
            raise serializers.ValidationError("Email address is required to login.")
        if password is None:
            raise serializers.ValidationError("A password is required to login.")
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError("User not found.")
        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")
        return {
            "user_id": str(user.pk),
            "email": user.email,
            "access_token": user.access_token,
            "refresh_token": user.refresh_token,
        }
