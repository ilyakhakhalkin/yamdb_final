from django.contrib import admin

from .common_fields import CommonAdmin
from .models import Category, Comment, Genre, GenreTitle, Review, Title


class CategoryAdmin(CommonAdmin):
    pass


class GenreAdmin(CommonAdmin):
    pass


class GenreTitleTabular(admin.TabularInline):
    model = GenreTitle


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'category',
        'description',
        'get_genres',
    )
    search_fields = (
        'pk',
        'name',
        'year',
        'category__name',
        'category__slug',
        'genre__name',
        'genre__slug',
    )
    inlines = [
        GenreTitleTabular,
    ]
    list_editable = ['category']

    def get_genres(self, obj):
        return ",\n".join([g.slug for g in obj.genre.all()])

    get_genres.short_description = 'Жанры'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'author',
        'text',
        'score',
        'pub_date',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'review',
        'text',
        'pub_date'
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
