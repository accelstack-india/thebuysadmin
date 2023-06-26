"""
URL configuration for demodjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from demodjango import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Signup, name=""),
    path('home', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('register', views.register, name="register"),
    path('footer', views.footer, name="footer"),
    path('header', views.header, name="header"),
    path('logout', views.logout, name="logout"),
    path('test', views.test, name="test"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('send_notification', views.send_notification, name="send_notification"),
    path('user_trade_history', views.user_trade_history, name="user_trade_history"),
]
