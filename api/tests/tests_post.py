from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import User, Tier, TierThumbnailSize


class PostImageListTest(APITestCase):
    """
    Test module for POST list API
    """

    def test_post_valid_ImageList(self):
        """
        Ensure that user can create a new image.
        """
        tier = Tier.objects.create(tier_name='test')
        TierThumbnailSize.objects.create(tier=tier, size=200)
        user = User.objects.create_user(username='test', password='test', tier=tier)
        self.client.force_login(user)
        response = self.client.post(reverse("image_list_create"),
                                    {"image": open(r"media/tests/test.png", "rb")})
        self.assertEqual(response.status_code, 201)

    def test_post_invalid_ImageList_with_original_image(self):
        """
        Ensure that user can't create a new image with original image.
        """
        tier = Tier.objects.create(tier_name='test', original_image=True)
        TierThumbnailSize.objects.create(tier=tier, size=200)
        user = User.objects.create_user(username='test', password='test', tier=tier)
        self.client.force_login(user)
        response = self.client.post(reverse("image_list_create"),
                                    {"image": open(r"media/tests/test.png", "rb")})
        self.assertEqual(response.status_code, 201)

    def test_post_invalid_ImageList_without_authorization(self):
        """
        Ensure that user can't create a new image if not authorized.
        """
        tier = Tier.objects.create(tier_name='test')
        TierThumbnailSize.objects.create(tier=tier, size=200)
        user = User.objects.create_user(username='test', password='test', tier=tier)
        response = self.client.post(reverse("image_list_create"),
                                    {"image": open(r"media/tests/test.png", "rb")})
        self.assertEqual(response.status_code, 401)

    def test_post_valid_ImageList_with_expiring_image(self):
        """
        Ensure that user can create a new image with expiring image.
        """
        tier = Tier.objects.create(tier_name='test', expiring_link=True)
        TierThumbnailSize.objects.create(tier=tier, size=200)
        user = User.objects.create_user(username='test', password='test', tier=tier)
        self.client.force_login(user)
        response = self.client.post(reverse("image_list_create"),
                                    {"image": open(r"media/tests/test.png", "rb"),
                                     "expiring_time": 300})
        self.assertEqual(response.status_code, 201)

    def test_post_invalid_ImageList_with_invalid_image(self):
        """
        Ensure that user can't create a new image if image is invalid.
        """
        tier = Tier.objects.create(tier_name='test')
        TierThumbnailSize.objects.create(tier=tier, size=200)
        user = User.objects.create_user(username='test', password='test', tier=tier)
        self.client.force_login(user)
        response = self.client.post(reverse("image_list_create"),
                                    {"image": open(r"media/tests/test.gif", "rb")})
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_ImageList_with_invalid_expiring_time(self):
        """
        Ensure that user can't create a new image if expiring time is invalid.
        """
        tier = Tier.objects.create(tier_name='test', expiring_link=True)
        TierThumbnailSize.objects.create(tier=tier, size=200)
        user = User.objects.create_user(username='test', password='test', tier=tier)
        self.client.force_login(user)
        response = self.client.post(reverse("image_list_create"),
                                    {"image": open(r"media/tests/test.png", "rb"),
                                     "expiring_time": 200})
        self.assertEqual(response.status_code, 400)
