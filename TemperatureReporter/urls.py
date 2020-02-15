from django.urls import path

from . import views

urlpatterns = [
    path('', views.sayHello, name='sayHello'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('login/', views.login, name='login'),
    path('TemperatureRecorder/', views.TemperatureRecorder, name='TemperatureRecorder'),


]
