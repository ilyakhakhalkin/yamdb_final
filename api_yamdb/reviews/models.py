from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .common_fields import CommonNameSlug, CommonRC
from .validators import validate_year


class Category(CommonNameSlug):
    class Meta(CommonNameSlug.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CommonNameSlug):
    class Meta(CommonNameSlug.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        through='GenreTitle',
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.XXL_FIELD,
        blank=False,
        null=False,
    )
    description = models.TextField(verbose_name='Описание')
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=(validate_year,),
        db_index=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'genre'],
                                    name='unique_genre-title')
        ]

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(CommonRC):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Название')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, message='Оценка не может быть меньше 1'),
            MaxValueValidator(10, message='Оценка не может быть больше 10')
        ],
        default=1)

    class Meta(CommonRC.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review')
        ]
        default_related_name = 'reviews'


class Comment(CommonRC):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Отзыв')

    class Meta(CommonRC.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
