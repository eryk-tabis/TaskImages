from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Properties for User model
    """
    tier = models.ForeignKey('Tier', on_delete=models.SET_NULL, null=True, blank=False)


class Tier(models.Model):
    """
    Properties for Tier model
    """
    tier_name = models.CharField(max_length=20)
    original_image = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.tier_name


class TierThumbnailSize(models.Model):
    """
    Properties for TierThumbnailSize model
    """
    tier = models.ForeignKey(Tier, related_name='sizes', on_delete=models.CASCADE)
    size = models.IntegerField()

    def __str__(self):
        return str(self.tier)
