from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import NewsletterSubscription


@shared_task
def send_news_notification(news_id):
    from .models import News
    news = News.objects.get(id=news_id)
    subscribers = NewsletterSubscription.objects.filter(category=news.category, subscribed=True)
    emails = [sub.user.email for sub in subscribers]

    send_mail(
        f'Новая новость: {news.title}',
        news.content,
        settings.DEFAULT_FROM_EMAIL,
        emails,
        fail_silently=False,
    )
