import datetime
from django.utils.crypto import get_random_string


def generate_filename():
    uid = get_random_string(length=16, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    date = datetime.datetime.now()
    return '%s-%s-%s_%s' % (date.year, date.month, date.day, uid)