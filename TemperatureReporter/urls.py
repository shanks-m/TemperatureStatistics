from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginPage, name='loginPage'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('employeeTemperatureSubmit', views.employeeTemperatureSubmit, name='employeeTemperatureSubmit'),
    path('teamTemperatureSubmit', views.teamTemperatureSubmit, name='teamTemperatureSubmit'),
    path('login/', views.login, name='login'),
    path('queryTeamTemperatureRecords', views.queryTeamTemperatureRecords, name='queryTeamTemperatureRecords'),
    path('temperatureRecorderPage/', views.TemperatureRecorder, name='temperatureRecorder'),
    path('getDailyReport/', views.GetDailyReport, name='getDailyReport'),
    path('getSubmitGroupInfo/', views.GetSubmitGroupInfo, name='getSubmitGroupInfo'),
]
