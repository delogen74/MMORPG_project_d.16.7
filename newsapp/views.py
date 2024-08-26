from django.shortcuts import render, get_object_or_404, redirect
from .models import Ad, News, Response, NewsCategory, NewsletterSubscription
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import AdForm, ResponseForm, ResponseFilterForm, AdFilterForm, SubscriptionForm
from django.shortcuts import render, redirect

@login_required
def my_ads(request):
    ads = Ad.objects.filter(author=request.user)

    if request.method == 'GET':
        filter_form = AdFilterForm(request.GET)
        if filter_form.is_valid():
            if filter_form.cleaned_data.get('category'):
                ads = ads.filter(category=filter_form.cleaned_data['category'])
            if filter_form.cleaned_data.get('date'):
                ads = ads.filter(created_at__date=filter_form.cleaned_data['date'])
            if filter_form.cleaned_data.get('title'):
                ads = ads.filter(title__icontains=filter_form.cleaned_data['title'])
    else:
        filter_form = AdFilterForm()

    context = {
        'ads': ads,
        'filter_form': filter_form
    }
    return render(request, 'newsapp/my_ads.html', context)



@login_required
def my_responses(request):
    responses = Response.objects.filter(ad__author=request.user)

    if request.method == 'GET':
        filter_form = ResponseFilterForm(request.GET)
        if filter_form.is_valid():
            if filter_form.cleaned_data.get('category'):
                responses = responses.filter(ad__category=filter_form.cleaned_data['category'])
            if filter_form.cleaned_data.get('date'):
                responses = responses.filter(created_at__date=filter_form.cleaned_data['date'])
            if filter_form.cleaned_data.get('title'):
                responses = responses.filter(ad__title__icontains=filter_form.cleaned_data['title'])
    else:
        filter_form = ResponseFilterForm()

    context = {
        'responses': responses,
        'filter_form': filter_form
    }
    return render(request, 'newsapp/my_responses.html', context)

@login_required
def accept_response(request, pk):
    response = get_object_or_404(Response, pk=pk)
    response.status = 'accepted'
    response.save()

    send_mail(
        'Ваш отклик принят',
        f'Ваш отклик на объявление "{response.ad.title}" был принят.',
        settings.DEFAULT_FROM_EMAIL,
        [response.author.email],
    )

    return redirect('responses_to_my_ads')

@login_required
def delete_response(request, pk):
    response = get_object_or_404(Response, pk=pk)
    response.delete()
    return redirect('responses_to_my_ads')

@login_required
def responses_to_my_ads(request):
    ads = Ad.objects.filter(author=request.user)
    responses = Response.objects.filter(ad__in=ads)
    return render(request, 'newsapp/responses_to_my_ads.html', {'responses': responses, 'ads': ads})

@login_required
def profile(request):
    return render(request, 'newsapp/profile.html')

def ad_list(request):
    ads = Ad.objects.all()

    if request.method == 'GET':
        filter_form = AdFilterForm(request.GET)
        if filter_form.is_valid():
            if filter_form.cleaned_data.get('category'):
                ads = ads.filter(category=filter_form.cleaned_data['category'])
            if filter_form.cleaned_data.get('date'):
                ads = ads.filter(created_at__date=filter_form.cleaned_data['date'])
            if filter_form.cleaned_data.get('title'):
                ads = ads.filter(title__icontains=filter_form.cleaned_data['title'])
    else:
        filter_form = AdFilterForm()

    context = {
        'ads': ads,
        'filter_form': filter_form
    }
    return render(request, 'newsapp/ad_list.html', context)


def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ad = ad
            response.author = request.user
            response.save()
            # Отправка уведомления автору объявления
            send_response_notification(ad, response)
            return render(request, 'newsapp/ad_detail.html', {'ad': ad})
    else:
        form = ResponseForm()
    return render(request, 'newsapp/ad_detail.html', {'ad': ad, 'form': form})

def news_list(request):
    news = News.objects.all()
    return render(request, 'newsapp/news_list.html', {'news': news})

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    return render(request, 'newsapp/news_detail.html', {'news_item': news_item})

def search(request):
    query = request.GET.get('q')
    results = Ad.objects.filter(title__icontains=query)
    return render(request, 'newsapp/search_results.html', {'results': results, 'query': query})

def contacts(request):
    return render(request, 'newsapp/contacts.html')

def main_info(request):
    return render(request, 'newsapp/main_info.html')


@login_required
def manage_subscription(request):
    categories = NewsCategory.objects.all()
    user_subscriptions = NewsletterSubscription.objects.filter(user=request.user, subscribed=True).values_list('category_id', flat=True)

    if request.method == 'POST':
        selected_categories = request.POST.getlist('categories')
        # Обновление подписок пользователя
        for category in categories:
            if str(category.id) in selected_categories:
                # Подписаться на категорию, если она выбрана
                NewsletterSubscription.objects.update_or_create(
                    user=request.user,
                    category=category,
                    defaults={'subscribed': True}
                )
            else:
                # Отписаться от категории, если она не выбрана
                NewsletterSubscription.objects.update_or_create(
                    user=request.user,
                    category=category,
                    defaults={'subscribed': False}
                )
        return redirect('subscription_success')  # Перенаправление на страницу успеха или обновления

    return render(request, 'newsapp/manage_subscription.html', {
        'categories': categories,
        'user_subscriptions': user_subscriptions,
    })

def send_response_notification(ad, response):
    subject = f'Новый отклик на ваше объявление: {ad.title}'
    message = f'У вас новый отклик на объявление "{ad.title}".\n\n{response.content}\n\nАвтор: {response.author.username}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [ad.author.email])

def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            return redirect('ad_list')
    else:
        form = AdForm()
    return render(request, 'newsapp/ad_form.html', {'form': form})

@login_required
def accept_response(request, pk):
    response = get_object_or_404(Response, pk=pk)
    response.accepted = True
    response.save()

    send_mail(
        'Ваш отклик принят',
        f'Ваш отклик на объявление "{response.ad.title}" был принят.',
        settings.DEFAULT_FROM_EMAIL,
        [response.author.email],
    )

    return redirect('responses_to_my_ads')

@login_required
def delete_response(request, pk):
    response = get_object_or_404(Response, pk=pk)
    response.delete()
    return redirect('responses_to_my_ads')


@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    return render(request, 'newsapp/ad_edit.html', {'form': form})


@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')
    return render(request, 'newsapp/ad_confirm_delete.html', {'ad': ad})

def home(request):
    return render(request, 'newsapp/home.html')

def subscription_success(request):
    return render(request, 'newsapp/subscription_success.html')