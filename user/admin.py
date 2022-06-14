from django.contrib import admin
from .models import User, Tier, TierThumbnailSize


class TierThumbnailSizeInLine(admin.TabularInline):
    """
    Properties in admin panel for ImageSizes model
    """
    model = TierThumbnailSize


@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    """
    Properties in admin panel for Image model
    """
    inlines = [TierThumbnailSizeInLine]
    list_display = ['tier_name']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Properties in admin panel for User model
    """