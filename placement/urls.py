from django.urls import path
from . import views

urlpatterns = [
    path(
        "dashboard/",
        views.placement_dashboard,
        name="placement_dashboard",
    ),
]