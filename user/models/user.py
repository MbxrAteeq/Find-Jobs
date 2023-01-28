from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import EmailValidator
from django.db import models
from core.base_model import BaseModel
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    """
    Custom user manager
    """
    def create_user(
            self,
            first_name,
            last_name,
            email,
            password=None,
    ):
        """
        Create and return User with an email, username and password.
        """
        if first_name is None:
            raise TypeError("Users must have a first name.")
        if last_name is None:
            raise TypeError("Users must have a last name.")
        if email is None:
            raise TypeError("Users must have an email address.")
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_enabled = False
        user.save()
        return user


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True, validators=[EmailValidator])
    password = models.CharField(max_length=128)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "password",
    ]
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def refresh_token(self):
        """
        Returns refresh token
        """
        return self.generate_jwt_token()["refresh"]

    @property
    def access_token(self):
        """
        Returns access token
        """
        return self.generate_jwt_token()["access"]

    def generate_jwt_token(self):
        """
        Generate new token
        """
        token = RefreshToken.for_user(self)
        return {
            "refresh": str(token),
            "access": str(token.access_token),
        }
