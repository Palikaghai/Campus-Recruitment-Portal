from django.db import models
from accounts.models import CustomUser


class PlacementOfficerProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    office_phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.get_full_name()