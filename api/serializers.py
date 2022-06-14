from rest_framework import serializers
from images.models import Image
from collections import OrderedDict
from django.utils import timezone


class ImageSizesSerializer(serializers.RelatedField):
    # returns a dict of image height and its url
    def to_representation(self, value):
        return {value.height: self.context['request'].build_absolute_uri(value.thumbnail)}


class ImageSerializer(serializers.ModelSerializer):
    thumbnails = ImageSizesSerializer(many=True, read_only=True, source='image_sizes')
    image = serializers.ImageField()
    image_expiring = serializers.SerializerMethodField(read_only=True)
    expiring_time = serializers.IntegerField()

    class Meta:
        model = Image
        fields = ['thumbnails', 'image', 'image_expiring', 'expiring_time']
        read_only_fields = ['thumbnails', 'image_expiring']

    def get_image_expiring(self, instance):
        """
        Returns base64 encoded image if user has expiring link
        """
        if not self.context['request'].user.tier.expiring_link:
            # if user is not be able to add expiring image, return None
            return
        if instance.image_expiring and timezone.now() < instance.create_time + timezone.timedelta(
                seconds=instance.expiring_time):
            # if expiring image is not None and expiring time is not expired return expiring image
            return instance.image_expiring.decode('utf-8')
        instance.image_expiring = None  # if image is expired, remove it from database

    def to_representation(self, instance):
        """
        Return a representation of instance checking if user can  see original image
        """
        result = super().to_representation(instance)
        if not self.context['request'].user.tier.original_image:
            # if user has no permission to see original image, return None
            result['image'] = None
        result['expiring_time'] = None  # removing expiring time from response
        return OrderedDict((key, result[key]) for key in result if result[key] is not None)

    def get_fields(self):
        """
        Returns fields for serializer checking if user can add expiring image
        """
        result = super().get_fields()
        if not self.context['request'].user.tier.expiring_link:
            # if user has no permission to add expiring image, remove expiring_time field
            result['expiring_time'] = None
            result['image_expiring'] = None
        return OrderedDict((key, result[key]) for key in result if result[key] is not None)

    def validate_image(self, value):
        """
        Validate image field
        """
        if value.name.split('.')[-1] not in ['png', 'jpg']:
            # if image format is not png or jpg, raise error
            raise serializers.ValidationError('Image extension must be png or jpg')
        return value

    def validate_expiring_time(self, value):
        """
        Validate expiring time field
        """
        if value < 300 or value > 30000:
            # if expiring time is not in range 300-30000, raise error
            raise serializers.ValidationError('Expiring time must be between 300 and 30000')
        return value

    def create(self, validated_data):
        return Image.objects.create(**validated_data, user=self.context['request'].user)
