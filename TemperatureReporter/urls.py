from django.urls import path

from . import views

urlpatterns = [
    path('', views.sayHello, name='sayHello'),
    path('login/', views.login, name='login'),

]
