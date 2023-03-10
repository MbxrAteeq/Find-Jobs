# Generated by Django 4.1.5 on 2023-01-28 14:29

import django.core.validators
from django.db import migrations, models
import uuid

from user.models import User


def create_superuser(*args):
    """
    Create superuser.
    """
    user = User(
        first_name="admin",
        last_name="test",
        email="admin@gmail.com",
        is_staff=True,
        is_superuser=True,
        is_enabled=True
    )
    user.set_password("123admin123")
    user.save()
    return


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("first_name", models.CharField(max_length=25)),
                ("last_name", models.CharField(max_length=25)),
                (
                    "email",
                    models.EmailField(
                        max_length=254,
                        unique=True,
                        validators=[django.core.validators.EmailValidator],
                    ),
                ),
                ("password", models.CharField(max_length=128)),
                ("is_deleted", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_enabled", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RunPython(create_superuser)
    ]
