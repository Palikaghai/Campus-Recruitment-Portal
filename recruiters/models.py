from django.db import models
from accounts.models import CustomUser


class RecruiterProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    company_name = models.CharField(max_length=150)
    designation = models.CharField(max_length=100)
    company_website = models.URLField(blank=True)

    def __str__(self):
        return self.company_name