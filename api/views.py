from .serializers import ImageSerializer
from images.models import Image
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class ImageListCreateAPI(generics.ListCreateAPIView):
    """
    A view that restore and create images
    """
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)
