from profile import Profile
from urllib.request import urlopen

from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string

from app.models import UserProfile


def get_avatar(backend, strategy, details, response,
        user=None, *args, **kwargs):
    url = None
    if backend.name == 'google-oauth2':
        url = response.get('picture')
    if url:
        avatar = urlopen(url)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        if not profile.profile_photo:
            profile.profile_photo.save(str(response.get('name', get_random_string(length=10)) + " social" + '.jpg').lower().replace(' ', '_'),
                                   ContentFile(avatar.read()))
        profile.save()