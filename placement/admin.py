from django.contrib import admin
from .models import (
    PlacementOfficerProfile,
    Company,
    PlacementDrive,
    Application
)


admin.site.register(PlacementOfficerProfile)
admin.site.register(Company)
admin.site.register(PlacementDrive)
admin.site.register(Application)