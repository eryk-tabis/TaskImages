from django.db import models
from PIL import Image as PILImage
from user.models import User
from django.core.validators import MinValueValidator
from base64 import b64encode


class Image(models.Model):
    """
    Model responsible for storing images
    """
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)
    expiring_time = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now=True)
    image_expiring = models.BinaryField(null=True, blank=True, editable=True)

    def save(self, *args, **kwargs):
        """
        Overriding save method
        """
        if self.user.tier.expiring_link and self.expiring_time is not None:
            # if user has expiring link and expiring time is not None then add expiring image
            self.image_expiring = b64encode(self.image.read())
        super().save()  # saving image
        for size in self.user.tier.sizes.all():
            # for each size in user's tier, create a thumbnail
            img = PILImage.open(self.image.path)  # opening image
            img = img.resize((self.image.width, size.size), PILImage.ANTIALIAS)  # resizing image
            img_format = self.image.path.split('.')[-1]  # getting image format
            thumbnail_path = self.image.path.replace(f'.{img_format}',
                                                     f'_{size.size}.{img_format}')  # creating thumbnail path
            img.save(thumbnail_path)  # saving image in different size
            ImageSizes.objects.create(image=self,
                                      thumbnail=self.image.url.replace(f'.{img_format}',
                                                                       f'_{size.size}.{img_format}'),
                                      height=img.height)  # creating ImageSizes object


class ImageSizes(models.Model):
    """
    Model responsible for storing image sizes
    """
    image = models.ForeignKey(Image, related_name='image_sizes', on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='images/')
    height = models.IntegerField(validators=[MinValueValidator(1)])
