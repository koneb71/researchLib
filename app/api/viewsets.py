from rest_framework import viewsets

from app.api.serializers import TagSerializer
from app.models import Tags


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer