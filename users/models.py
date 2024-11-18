from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100)
    email_notifications = models.BooleanField(default=False)
    sms_notifications = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
