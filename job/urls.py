from django.urls import path
from job.views import JobAPIView, UserApplicationAPIView

urlpatterns = [
    path(
        "",
        JobAPIView.as_view(
            {'get': 'list', "post": "create", "put": "update", "delete": "destroy"}
        ),
        name="job"
    ),
    path(
        "user_application/",
        UserApplicationAPIView.as_view({'get': 'list', "post": "create"}),
        name="user_application"
    )
]
