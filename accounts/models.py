from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractUser):

    ROLE_CHOICES = [
        ("student", "Student"),
        ("recruiter", "Recruiter"),
        ("placement_officer", "Placement Officer"),
    ]

    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )

    role = models.CharField(
        max_length=25,
        choices=ROLE_CHOICES,
        default="student",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email