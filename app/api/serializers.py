from rest_framework import serializers

from app.models import Tags


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = ('name',)