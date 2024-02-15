from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string

from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def post_created(instance, sender, **kwargs):
    if kwargs['action'] == 'post_add':
        subscribers_emails = []

        for category in instance.category.all():
            subscribers_emails += User.objects.filter(subscriptions__category=category).values_list('email', flat=True)

        subject = f'Новая публикация в категории {instance.category}'

        context = {
            'post_title': instance.post_title,
            'post_preview': instance.preview(),
            'post_url': f'{settings.SITE_URL}/news/{instance.id}/'
        }

        text_content = (
                f'Заголовок: {instance.post_title}\n'
                f'Текст: {instance.preview()}\n\n'
                f'Ссылка на публикацию: http://127.0.0.1:8000{instance.get_absolute_url()}'
            )
        html_content = render_to_string(
            'post_created_email.html', context
            )

        for email in subscribers_emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
