from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from ads.models import Ad
from accounts.models import Author
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from celery import shared_task
import time


def notify(user, html_template, ads):
    email = user.email
    name = user.username
    html_content = render_to_string(
        html_template,
        {
            'ads': ads,
            'name': name,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Объявления портала ad-b.test.com',
        from_email=settings.SERVER_EMAIL,
        to=[email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def weekly_ads_notify():
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    ads = Ad.objects.filter(creation_datetime__gte=week_ago, creation_datetime__lt=now).order_by('-creation_datetime')
    for author in Author.objects.all():
        print(f'{author} {ads}')
        if author and ads:
            notify(author.user, 'weekly_ads_notice.html', ads)
