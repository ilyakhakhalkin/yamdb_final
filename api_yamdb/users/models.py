from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    username = models.CharField(
        'username', max_length=settings.L_FIELD, unique=True,
        help_text=('Required. 150 characters or fewer. Letters, digits'
                   'and @/./+/-/_ only.'),
        validators=[validate_username]
    )
    email = models.EmailField('E-Mail', max_length=settings.XL_FIELD,
                              blank=False, unique=True)
    first_name = models.CharField('Имя', max_length=settings.L_FIELD,
                                  blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Уровень прав',
        max_length=max(len(role) for role, text in ROLE_CHOICES),
        choices=ROLE_CHOICES, default=USER
    )
    confirmation_code = models.IntegerField('Код подтверждения', blank=False,
                                            default=0)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_superuser or self.is_staff or self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
