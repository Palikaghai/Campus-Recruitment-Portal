from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("notifications/", views.notifications_list, name="notifications_list"),
    path("notifications/<int:notification_id>/read/", views.mark_notification_read, name="mark_notification_read"),
    path("search/", views.global_search, name="global_search"),
    path("settings/", views.user_settings, name="user_settings"),
]