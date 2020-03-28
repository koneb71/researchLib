from urllib.error import HTTPError
from urllib.request import urlopen

from social_core.backends import google

from app.models import UserProfile


def new_users_handler(sender, user, response, details, **kwargs):
    user.is_new = True
    if user.is_new:
        if "id" in response:

            from django.template.defaultfilters import slugify
            from django.core.files.base import ContentFile

            try:
                url = None
                if sender == google.GoogleOAuth2 and "picture" in response:
                    url = response["picture"]

                if url:
                    avatar = urlopen(url)
                    profile = UserProfile(user=user)

                    profile.profile_photo.save(slugify(user.username + " social") + '.jpg',
                                               ContentFile(avatar.read()))

                    profile.save()

            except HTTPError:
                pass

    return False