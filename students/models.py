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

    skills = models.TextField(blank=True, help_text="Comma separated skills")
    projects = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def profile_completion_percentage(self):
        total_points = 6
        completed = 0
        if self.registration_number:
            completed += 1
        if self.department and self.batch and self.cgpa:
            completed += 1
        if self.resume:
            completed += 1
        if self.skills and self.skills.strip():
            completed += 1
        if self.projects and self.projects.strip():
            completed += 1
        if self.certifications and self.certifications.strip():
            completed += 1
        return int((completed / total_points) * 100)