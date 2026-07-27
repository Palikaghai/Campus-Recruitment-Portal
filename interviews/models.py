from django.db import models
from placement.models import Application


class Interview(models.Model):

    INTERVIEW_TYPES = [
        ("Technical", "Technical"),
        ("HR", "HR"),
        ("Managerial", "Managerial"),
    ]

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE
    )

    interview_type = models.CharField(
        max_length=20,
        choices=INTERVIEW_TYPES
    )

    interview_date = models.DateField()

    interview_time = models.TimeField()

    mode = models.CharField(
        max_length=20,
        choices=[
            ("Online", "Online"),
            ("Offline", "Offline"),
        ]
    )

    meeting_link = models.URLField(
        blank=True,
        null=True
    )

    venue = models.CharField(
        max_length=255,
        blank=True
    )

    interviewer = models.CharField(
        max_length=100
    )

    def __str__(self):
        return f"{self.application.drive.company.name} Interview"