from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.core.cache import cache
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.utils.text import slugify
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import int_to_base36, base36_to_int
from django.utils.crypto import constant_time_compare, salted_hmac

from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from rest_framework.reverse import reverse
from rest_framework.exceptions import ValidationError

from neomodel import db, DoesNotExist
from unidecode import unidecode


def generate_username(first_name, last_name):
    profile_count = User.objects.filter(first_name__iexact = first_name).filter(
        last_name__iexact = last_name).count()
    username = "%s_%s" % (first_name.lower(), last_name.lower())

    if len(username) > 30:
        username = username[:30]
        profile_count = User.objects.filter(username__iexact = username).count()

        if profile_count > 0:
            username = username[:(30 - profile_count)] + str(profile_count)

    elif len(username) < 30 and profile_count == 0:
        username = "%s_%s" % (
            (''.join(e for e in first_name if e.isalnum())).lower(),
            (''.join(e for e in last_name if e.isalnum())).lower())
    else:
        username = "%s_%s%d" % (
            (''.join(e for e in first_name if e.isalnum())).lower(),
            (''.join(e for e in last_name if e.isalnum())).lower(),
            profile_count)
    try:
        username = unidecode (unicode(username, "utf-8"))
    except TypeError:
        # Handles cases where the username is already in unicode format
        username = unidecode(username)
    return username