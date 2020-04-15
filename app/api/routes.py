from rest_framework import routers

from app.api.viewsets import TagViewSet

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet)