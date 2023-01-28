from rest_framework import serializers

from job.models import Job, UserApplication
from job.serializers.user_application_serializer import UserApplicationSerializer
from user.serializers.user_serializer import UserSerializer


class JobSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization of Job objects.
    """

    class Meta:
        model = Job
        fields = "__all__"

    def create(self, validated_data):
        return Job.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("user")
        return super().update(instance, validated_data)


class JobWithUserApplicationsSerializer(serializers.ModelSerializer):
    user_applications = serializers.SerializerMethodField(read_only=True, method_name="get_user_applications")

    class Meta:
        model = Job
        fields = "__all__"

    def get_user_applications(self, obj):
        return UserApplicationSerializer(UserApplication.objects.filter(job__id=obj.id).all(), many=True).data


class UserApplicationDetailSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserialization of UserApplication objects.
    """
    job = JobSerializer()
    user = UserSerializer()

    class Meta:
        model = UserApplication
        fields = "__all__"
