from django.db import models
from django.utils import timezone
from accounts.models import CustomUser


class Notification(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=50,
        default="info",
        choices=[
            ("info", "Info"),
            ("success", "Success"),
            ("warning", "Warning"),
            ("danger", "Danger"),
        ]
    )
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.title}"


def notify_user(user, title, message, notification_type="info", link=""):
    if user:
        Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            link=link
        )

