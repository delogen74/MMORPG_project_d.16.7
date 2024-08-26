# Generated by Django 5.1 on 2024-08-26 12:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0003_alter_ad_options_alter_category_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='response',
            name='accepted',
        ),
        migrations.AddField(
            model_name='response',
            name='status',
            field=models.CharField(choices=[('pending', 'На согласовании'), ('accepted', 'Принят'), ('deleted', 'Удален')], default='pending', max_length=10, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ad',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsapp.category'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='ad',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ad',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='ad_images/'),
        ),
        migrations.AlterField(
            model_name='ad',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='ad',
            name='videos',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='content',
            field=models.TextField(verbose_name='Текст отклика'),
        ),
    ]
