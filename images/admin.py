from django.contrib import admin
from .models import Image, ImageSizes


class ImageSizesInLine(admin.TabularInline):
    """
    Properties in admin panel for ImageSizes model
    """
    model = ImageSizes
    list_display = ['thumbnail']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Properties in admin panel for Image model
    """
    inlines = [ImageSizesInLine]