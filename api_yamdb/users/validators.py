import re

from django.conf import settings
from django.core.exceptions import ValidationError

USERNAME_REGEX = r'^[\w.@+-]+$'


def validate_username(username):
    invalid_symbols = ''.join(set(re.sub(USERNAME_REGEX, '', username)))
    if invalid_symbols:
        raise ValidationError(f'Напишите username без {invalid_symbols}')
    if username in settings.USERNAME_BLACKLIST:
        raise ValidationError(
            'Такой username выбрать нельзя, попробуйте другой.'
        )
