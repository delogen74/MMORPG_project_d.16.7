from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class NewsCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ad(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='ad_images/', blank=True, null=True)
    videos = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, verbose_name='Категория')  # Правильная связь с NewsCategory
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    images = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name='Изображения')
    videos = models.URLField(blank=True, null=True, verbose_name='Видео')
    published_at = models.DateTimeField(auto_now_add=True)

    def send_news_notification(self):
        subscribers = NewsletterSubscription.objects.filter(category=self.category, subscribed=True)
        emails = [sub.user.email for sub in subscribers]

        send_mail(
            f'Новая новость в категории {self.category.name}: {self.title}',
            f'Прочитать новость можно по ссылке: {self.get_absolute_url()}',
            settings.DEFAULT_FROM_EMAIL,
            emails,
            fail_silently=False,
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Response(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На согласовании'),
        ('accepted', 'Принят'),
        ('deleted', 'Удален'),
    ]

    ad = models.ForeignKey(Ad, related_name='responses', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Отклик на {self.ad.title} от {self.author.username}'

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"

    def accept(self):
        self.status = 'accepted'
        self.save()
        self.send_notification()

    def delete_response(self):
        self.status = 'deleted'
        self.save()

    def send_notification(self):
        subject = f'Ваш отклик на объявление "{self.ad.title}" был принят'
        message = f'Ваш отклик на объявление "{self.ad.title}" был принят автором объявления.'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.author.email])

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    message = models.TextField(verbose_name='Сообщение')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')

    def __str__(self):
        return f'Уведомление для {self.user.username}'

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

class NewsletterSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='newsletter_subscriptions')
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='subscriptions')
    subscribed = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.category.name} - {"Subscribed" if self.subscribed else "Unsubscribed"}'
