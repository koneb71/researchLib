from django.contrib.auth import get_user


def extra(request):
    user = get_user(request)
    if not user.is_anonymous:
        return {
            'profile_picture': user.profile_photo,
        }
    return {}