from django.urls import path
from .import views

urlpatterns = [

    path('', views.home, name="home"),
    path('contact.html', views.contact, name="contact"),
    path('about.html', views.about, name="about"),
    path('booknow.html', views.booknow, name="booknow"),
    path('mainpage.html', views.mainpage, name="mainpage"),
    path('login.html', views.login, name="login"),
    path('settings.html', views.settings, name="settings"),
    path('settings success.html', views.settings_success, name="settings success"),
    path('home.html', views.logout, name="logout"),
    path('result.html', views.result, name="result"),
    path('ratings.html', views.ratings, name="ratings"),
    path('rate success.html', views.rate_success, name="rate success"),
    path('update success.html', views.update_success, name="update success"),
    path('update.html', views.update, name="update"),
]
