from django.urls import path
from . import views


app_name = 'base'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.login_user, name = "login"),
    path('logout/', views.logout_user, name = "logout"),
    path('register/', views.register_user, name = "register"),
    path('show-profile/<str:pk>/', views.show_profile, name = 'show-profile'),
    path('search/', views.search, name = 'search'),
    path('show-chats/', views.show_chats, name = 'show-chats'),
    path('show-messages/<str:pk>', views.show_messages, name = 'show-messages'),
    path('send-message/', views.send_message, name = 'send-message'),
    path('create-post/', views.create_post, name = 'create-post'),
    path('follow/<str:pk>/', views.follow, name = 'follow'),
    path('unfollow/<str:pk>/', views.unfollow, name = 'unfollow'),
    path('settings/', views.settings, name = 'settings'),
]