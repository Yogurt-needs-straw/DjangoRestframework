"""
URL configuration for DjangoRestframework project.

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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from drfdemo import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('user/', views.UserView.as_view()),
    path('order/', views.OrderView.as_view()),
    path('avatar/', views.AvatarView.as_view()),


    path('home/', views.HomeView.as_view(), name='home'),
    path('api/<str:version>/home/', views.HomeToView.as_view(), name='homeTo'),
    path('api/home/', views.HomeTiView.as_view(), name='homeTi'),

    path('api/<str:version>/img/', views.ImgView.as_view(), name='img'),

    path('api/<str:version>/depart/', views.DepartView.as_view(), name='depart'),

    path('api/<str:version>/user/', views.UserView2.as_view()),

    path('api/<str:version>/depart2/', views.DepartView2.as_view()),
    path('api/<str:version>/us/', views.UsView.as_view()),
    path('api/<str:version>/nb/', views.NbView.as_view()),
    path('api/<str:version>/sb/', views.SbView.as_view()),

]
