from django import forms
from .models import Ad, Response, Category, NewsletterSubscription, NewsCategory

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'content', 'category', 'images', 'videos']
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'category': 'Категория',
            'images': 'Изображения',
            'videos': 'Видео',
        }

    def save(self, *args, **kwargs):
        ad = super().save(*args, **kwargs)
        if not self.cleaned_data.get('images'):
            ad.images.delete(save=False)
        return ad

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']
        labels = {
            'content': 'Ваш отклик',
        }


class ResponseFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Категория')
    date = forms.DateField(required=False, label='Дата')
    title = forms.CharField(max_length=100, required=False, label='Название объявления')


class AdFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Все категории",
        label="Категория"
    )
    date = forms.DateField(required=False, widget=forms.SelectDateWidget, label="Дата")
    title = forms.CharField(required=False, label="Название")


class SubscriptionForm(forms.Form):
    category = forms.ModelChoiceField(queryset=NewsCategory.objects.all(), label='Выберите категорию')
    subscribed = forms.ChoiceField(choices=[(True, 'Подписаться'), (False, 'Отписаться')], label='Действие')