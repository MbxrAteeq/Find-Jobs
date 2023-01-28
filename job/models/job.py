from django.db import models
from core.base_model import BaseModel
from user.models import User


class Job(BaseModel):
    """
    Job Application
    """
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=(
        ("Full_Time", "full_time"),
        ("Part_Time", "part_time"),
        ("Internship", "internship"),
    ), default="full_time")
    occupied = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
