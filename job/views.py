from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from custom_handlers.custom_exceptions import NotOwner, UnProcessableEntity
from .filters import JobFilter
from .models import Job, UserApplication
from .serializers.job_serializer import (
    JobSerializer,
    JobWithUserApplicationsSerializer,
    UserApplicationDetailSerializer
)
from .serializers.user_application_serializer import UserApplicationSerializer
from django.shortcuts import get_object_or_404


class JobAPIView(ModelViewSet):
    queryset = Job.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = JobSerializer
    filterset_class = JobFilter
    search_fields = ("id", "title", "job_type", "location", "occupied", "user")
    ordering = ("created_at",)

    def get_permissions(self):
        if self.action in ["create", "update", "delete", "destroy"]:
            return [IsAdminUser(), ]
        return [IsAuthenticated(), ]

    def get_serializer_class(self):
        if self.action in ["list", "get"] and self.request.user.is_staff:
            return JobWithUserApplicationsSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        job = request.data
        job["user"] = request.user.id
        serializer = self.serializer_class(data=job)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "Job has been created"
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        job = request.data
        instance = get_object_or_404(Job, id=job.get("id"))
        if instance.user.id != request.user.id:
            raise NotOwner()
        serializer = self.get_serializer(instance, data=job, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "Job has been updated"
            },
            status=status.HTTP_201_CREATED,
        )


class UserApplicationAPIView(ModelViewSet):
    queryset = UserApplication.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UserApplicationSerializer

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_staff:
            return self.queryset
        return UserApplication.objects.filter(user=current_user)

    def get_serializer_class(self):
        if self.action in ["list", "get"]:
            return UserApplicationDetailSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        user_application = request.data
        job = get_object_or_404(Job, id=user_application.get("job"))
        if not job:
            raise UnProcessableEntity("Invalid job ID")
        if job.occupied:
            raise UnProcessableEntity("Job already occupied")
        user_application["user"] = request.user.id
        serializer = self.serializer_class(data=user_application)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "User Application has been created"
            },
            status=status.HTTP_201_CREATED,
        )
