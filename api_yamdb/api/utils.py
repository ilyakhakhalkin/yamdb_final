from django.conf import settings
from django.core.mail import send_mail

MSG = ('Вы получили это письмо, поскольку этот электронный ящик был указан при'
       'регистрации на сайте YaMDB.\nВаш код подтверждения: {code}. Отправьте'
       'POST-запрос с вашим username и кодом на эндпоинт /api/v1/auth/token/,'
       '\nгде получите токен. Он позволит работать с API на правах'
       'зарегистрированного пользователя.')


def code_mail(code, email):
    """Посылает письмо на ящик с кодом."""
    send_mail(
        subject='YaMDB Confirmation code',
        message=MSG.format(code=code),
        from_email=settings.ADMIN_MAIL,
        recipient_list=[f'{email}'],
        fail_silently=False,
    )
