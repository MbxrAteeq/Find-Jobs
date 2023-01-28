from rest_framework import serializers
from job.models.user_application import UserApplication


class UserApplicationSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization of UserApplication objects.
    """

    class Meta:
        model = UserApplication
        fields = "__all__"

    def create(self, validated_data):
        return UserApplication.objects.create(**validated_data)
