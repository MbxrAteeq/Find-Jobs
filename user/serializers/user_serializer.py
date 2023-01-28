from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization of User objects.
    """
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
        ]
        read_only_fields = ["access_token"]

    def update(self, instance, validated_data):
        """
        Performs an update on a User.
        """
        password = validated_data.pop("password", None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
