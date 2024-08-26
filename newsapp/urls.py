from django.urls import path
from . import views
from .views import ad_list, ad_detail, ad_create, ad_edit, ad_delete, my_ads, my_responses, responses_to_my_ads, accept_response, delete_response, manage_subscription, subscription_success

urlpatterns = [
    path('', views.home, name='home'),
    path('ads/', ad_list, name='ad_list'),
    path('ads/create/', ad_create, name='ad_create'),
    path('ads/<int:pk>/', ad_detail, name='ad_detail'),
    path('ads/<int:pk>/edit/', ad_edit, name='ad_edit'),
    path('ads/<int:pk>/delete/', ad_delete, name='ad_delete'),
    path('my_ads/', my_ads, name='my_ads'),
    path('my_responses/', my_responses, name='my_responses'),
    path('responses/<int:pk>/accept/', accept_response, name='accept_response'),
    path('responses/<int:pk>/delete/', delete_response, name='delete_response'),
    path('responses_to_my_ads/', responses_to_my_ads, name='responses_to_my_ads'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('profile/', views.profile, name='profile'),
    path('contacts/', views.contacts, name='contacts'),
    path('main-info/', views.main_info, name='info'),
    path('subscription/', manage_subscription, name='manage_subscription'),
    path('subscription_success/', subscription_success, name='subscription_success'),
]
