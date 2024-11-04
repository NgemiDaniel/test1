from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('seller', 'seller'),
        ('delivery', 'delivery'),
        ('client', 'Client'),
        ('superuser', 'Superuser'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def is_manager(self):
        return self.role == 'manager'

    def is_video_editor(self):
        return self.role == 'seller'

    def is_sales(self):
        return self.role == 'delivery'

    def is_client(self):
        return self.role == 'client'

    # No need for a separate is_superuser method, use the built-in

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.user.username}'s Profile"