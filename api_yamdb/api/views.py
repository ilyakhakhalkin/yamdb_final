import random

from django.db import IntegrityError
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .mixins import PermissionSearchLookupMixin
from .permissions import Admin, ReadOrAdmin, ReadOrAuthorModerAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenSerializer, User, UserMeSerializer,
                          UserSerializer)
from .utils import code_mail


class CategoryViewSet(PermissionSearchLookupMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(PermissionSearchLookupMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (ReadOrAdmin,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering_fields = ['name', 'year', 'category', 'genre']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReadOrAuthorModerAdmin,)

    def get_title(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user,
                               title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ReadOrAuthorModerAdmin,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class SignUpView(APIView):
    user_validation_data = (
        ('email', 'Этот email уже зарегистрирован'),
        ('username', 'Этот username уже используется')
    )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user, _ = User.objects.get_or_create(username=data['username'],
                                                 email=data['email'])
        except IntegrityError as error:
            for field, msg in self.user_validation_data:
                if field in str(error):
                    return Response(msg, status.HTTP_400_BAD_REQUEST)
        code = random.randint(100000, 999999)
        code_mail(code, data['email'])
        user.confirmation_code = code
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if data['confirmation_code'] != 0:
            if data['confirmation_code'] == user.confirmation_code:
                return Response(
                    {'access': str(RefreshToken.for_user(user).access_token)},
                    status=status.HTTP_201_CREATED)
        return Response('Код подтверждения неверен',
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [Admin]
    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserMeSerializer(request.user)
            return Response(serializer.data)
        serializer = UserMeSerializer(request.user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
