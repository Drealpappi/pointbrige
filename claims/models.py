from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create Your Models here

class ClaimHistory(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='claims'
    )

    points_claimed = models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} claimed {self.points_claimed}"