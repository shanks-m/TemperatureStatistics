from django.urls import path

from . import views

urlpatterns = [
    path('', views.sayHello, name='sayHello'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('employeeTemperatureSubmit', views.employeeTemperatureSubmit, name='employeeTemperatureSubmit'),
    path('employeeSubmitTest', views.employeeSubmitTest, name='employeeSubmitTest'),
    path('login/', views.login, name='login'),
    path('getEmployeeTemperatureByTeamId', views.getEmployeeTemperatureByTeamId, name='getEmployeeTemperatureByTeamId'),
    path('TemperatureRecorder/', views.TemperatureRecorder, name='TemperatureRecorder'),
]
