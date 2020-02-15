from django.urls import path

from . import views

urlpatterns = [
    path('', views.sayHello, name='sayHello'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('employeeTemperatureSubmit', views.employeeTemperatureSubmit, name='employeeTemperatureSubmit'),
    path('teamTemperatureSubmit', views.teamTemperatureSubmit, name='teamTemperatureSubmit'),
    path('employeeSubmitTest', views.employeeSubmitTest, name='employeeSubmitTest'),
    path('teamSubmitTest', views.teamSubmitTest, name='teamSubmitTest'),
    path('login/', views.login, name='login'),
    path('queryTeamTemperatureRecords/', views.queryTeamTemperatureRecords, name='login'),
    path('TemperatureRecorder/', views.TemperatureRecorder, name='TemperatureRecorder'),

]
