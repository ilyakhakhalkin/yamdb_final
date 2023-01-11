from django.conf import settings
from django.core.validators import MaxValueValidator
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import validate_username


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    year = serializers.IntegerField(
        validators=[MaxValueValidator(timezone.now().year)],
    )

    class Meta:
        fields = '__all__'
        model = Title

    def to_representation(self, value):
        return TitleReadSerializer(self.instance).data


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title
        read_only_fields = ['__all__']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = 'id', 'author', 'text', 'score', 'pub_date'
        model = Review
        read_only_fields = ('author',)

    def validate(self, validated_data):
        if self.context['request'].method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            author = self.context['request'].user
            if Review.objects.filter(
                    author=author,
                    title_id=title_id).exists():
                raise serializers.ValidationError('Вы уже отозвались, хватит.')
        return validated_data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = 'id', 'text', 'author', 'pub_date'
        model = Comment


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.L_FIELD,
        validators=[validate_username]
    )
    email = serializers.EmailField(max_length=settings.XL_FIELD)

    class Meta():
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.L_FIELD, validators=[validate_username],
        required=True
    )
    confirmation_code = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message=('Этот email уже зарегистрирован')
        )])
    username = serializers.CharField(validators=[
        validate_username, UniqueValidator(
            queryset=User.objects.all(),
            message=('Этот username уже используется')
        )
    ])

    class Meta():
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class UserMeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ['role']
