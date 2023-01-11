from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOrAdmin(BasePermission):  # категории жанры titles
    """Позволяет читать всем, добавление новых записей доступно админам.
    Используеся в /titles/."""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin)


class ReadOrAuthorModerAdmin(BasePermission):  # для ревью и коментов
    """Позволяет читать всем, добавление новых записей доступно
    зарегистрированным пользователям, а изменение существующих записей
    доступно их авторам и админам. Используется в /reviews/ и /comments/."""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and (obj.author == request.user or request.user.is_admin
                     or request.user.is_moderator))


class Admin(BasePermission):
    """Проверяет обратившегося, админ ли он. Используется в /users/."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
