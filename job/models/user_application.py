from django.db import models
from django.core.validators import FileExtensionValidator
from core.base_model import BaseModel
from user.models import User
from job.models.job import Job


class UserApplication(BaseModel):
    """
    User Applications for a Job
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resume", validators=[FileExtensionValidator(["pdf", "doc", "docx"])])

    def __str__(self):
        return self.job.title
