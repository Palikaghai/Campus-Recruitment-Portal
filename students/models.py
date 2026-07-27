from django.db import models
from accounts.models import CustomUser


class StudentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    registration_number = models.CharField(
        max_length=20,
        unique=True
    )

    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )

    department = models.CharField(max_length=100)

    batch = models.IntegerField()

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    def __str__(self):
        return self.user.get_full_name()