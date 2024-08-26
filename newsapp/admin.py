from django.contrib import admin
from .models import Category, Ad, News, Response, Notification, NewsCategory, NewsletterSubscription

admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(News)
admin.site.register(Response)
admin.site.register(Notification)
admin.site.register(NewsCategory)
admin.site.register(NewsletterSubscription)

admin.site.site_header = "Панель администратора"
admin.site.site_title = "Администрирование сайта"
admin.site.index_title = "Добро пожаловать в административную панель"
