from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import User, Tier, TierThumbnailSize
from images.models import Image


class GetImageListTest(APITestCase):
    """
    Test module for GET list API
    """

    def test_get_valid_ImageList(self):
        """
        Ensure that user can retrieve a list of images.
        """
        tier = Tier.objects.create(tier_name='test')
        TierThumbnailSize.objects.create(tier=tier, size=200)
        user = User.objects.create_user(username='test', password='test', tier=tier)
        Image.objects.create(image=r"tests/test.png", user=user)
        self.client.force_login(user)
        response = self.client.get(reverse("image_list_create"))
        self.assertEqual(response.status_code, 200)

    def test_get_valid_ImageList_with_original_image(self):
        """
        Ensure that user can retrieve a list of images with original images.
        """
        tier = Tier.objects.create(tier_name='test', original_image=True)
        TierThumbnailSize.objects.create(tier=tier, size=300)
        user = User.objects.create_user(username='test', password='test',
                                        tier=tier)
        Image.objects.create(image=r"tests/test.png", user=user)
        self.client.force_login(user)
        response = self.client.get(reverse("image_list_create"))
        self.assertEqual(response.status_code, 200)

    def test_get_valid_ImageList_with_expiring_link(self):
        """
        Ensure that user can retrieve a list of images with expiring link.
        """
        tier = Tier.objects.create(tier_name='test', expiring_link=True)
        TierThumbnailSize.objects.create(tier=tier, size=200)
        user = User.objects.create_user(username='test', password='test', tier=tier)
        Image.objects.create(image=r"tests/test.png",
                             user=user, expiring_time=300)

        self.client.force_login(user)
        response = self.client.get(reverse("image_list_create"))
        self.assertEqual(response.status_code, 200)

    def test_get_valid_ImageList_with_original_image_and_expiring_link(self):
        """
        Ensure that user can retrieve a list of images with original image and expiring link.
        """
        tier = Tier.objects.create(tier_name='test', original_image=False, expiring_link=False)
        TierThumbnailSize.objects.create(tier=tier, size=200)
        user = User.objects.create_user(username='test', password='test', tier=tier)
        Image.objects.create(image=r"tests/test.png",
                             user=user, expiring_time=300)
        self.client.force_login(user)
        response = self.client.get(reverse("image_list_create"))
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_ImageList_not_authorized(self):
        """
        Ensure that user can't retrieve a list of images if not authorized.
        """
        tier = Tier.objects.create(tier_name='test',
                                   original_image=True, expiring_link=False)
        TierThumbnailSize.objects.create(tier=tier, size=200)
        user = User.objects.create_user(username='test', password='test', tier=tier)
        Image.objects.create(image=r"tests/test.png", user=user)
        response = self.client.get(reverse("image_list_create"), format="json")
        self.assertEqual(response.status_code, 401)
