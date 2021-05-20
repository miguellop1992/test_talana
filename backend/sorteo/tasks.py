from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

from backend.sorteo.models import User
from django.template import engines


@shared_task(bind=True)
def user_verify(self, email, localhost):
    user = User.objects.get(email=email)

    subject = 'Verificacion de correo'
    message = render_to_string('verify.html', {'link': (localhost + user.get_link())})

    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        reply_to=['another@example.com'],
    )
    email.content_subtype = "html"
    email.send()
