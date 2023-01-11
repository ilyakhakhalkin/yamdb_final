from django.conf import settings
from django.contrib import admin
from django.db import models

from users.models import User


class CommonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')


class CommonNameSlug(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.XXL_FIELD,
        blank=False,
        null=False,
    )
    slug = models.SlugField(
        verbose_name='Адрес',
        max_length=settings.S_FIELD,
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name', '-id',)

    def __str__(self):
        return self.slug


class CommonRC(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:20]
