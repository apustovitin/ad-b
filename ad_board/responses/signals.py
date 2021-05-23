from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .models import Response
from ads.models import Ad
from accounts.models import Author
from django.contrib.auth.models import User


@receiver(post_save, sender=Response)
def notify_about_add_response(sender, instance, created, **kwargs):
    response = instance
    ad = response.ad
    if response.status == 'NEW':
        ad_author = ad.author.user
        email = ad_author.email
        name = ad_author.username
        html = 'responses/response_notice.html'
    elif response.status == 'ACP':
        response_author = response.author.user
        email = response_author.email
        name = response_author.username
        html = 'responses/response_accept_notice.html'
    html_content = render_to_string( 
        html,
        {
            'response': response,
            'ad': ad,
            'name': name,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Отклики на объявления ad-b.test.com',
        from_email=settings.SERVER_EMAIL,
        to=[email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# @receiver(m2m_changed, sender=Post.category.through)
# def notify_subscribers_about_news(sender, instance, action, reverse, model, pk_set, **kwargs):
#     if action == "post_add":
#         subscribers_info = instance.get_subscribers_info_by_post()
#         # pc = PostCategory.objects.filter(post=instance)
#         print(f'si: {subscribers_info}')
#         if subscribers_info:
#             for subscriber_info in subscribers_info:
#                 email = subscriber_info['email']
#                 name = subscriber_info['name']
#                 category = subscriber_info['category']
#                 html_content = render_to_string( 
#                     'news_added.html',
#                     {
#                         'one_news': instance,
#                         'name': name,
#                         'category': category,
#                     }
#                 )
#                 msg = EmailMultiAlternatives(
#                     subject=f'Новости портала np-d.test.com',
#                     body=f'Здравствуйте, {name}. Новая статья в категории {category}!',
#                     from_email=settings.SERVER_EMAIL,
#                     to=[email],
#                 )
#                 msg.attach_alternative(html_content, "text/html")
#                 msg.send()

# def send_custom_mail(subject, message, recipient_list):
#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=settings.SERVER_EMAIL,
#         recipient_list=recipient_list
#     )
# 
# @receiver(m2m_changed, sender=Category.subscribers.through)
# def subscribtion_add_notify(sender, instance, action, reverse, model, pk_set, **kwargs):
#     category = instance
#     user = User.objects.get(id=pk_set.copy().pop())
#     name = user.first_name or user.username
#     if action == "post_add":
#         subject = f'Оповещение о подписке'
#         message = f'Здравствуйте, {name}.' \
#                   f'Вы были подписались на оповещение о свежих новостях в категории {category} портала np-d.test.com.'
#         send_custom_mail(subject, message, [f'{user.email}', ])
#     if action == "post_remove":
#         subject = f'Оповещение об отписке'
#         message = f'Здравствуйте, {name}.' \
#                   f'Вы отписались от оповещения о свежих новостях в категории {category} портала np-d.test.com.'
#         send_custom_mail(subject, message, [f'{user.email}', ])
