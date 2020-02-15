from django.shortcuts import render
from TemperatureReporter.models import Employees, Temperatures, SubmitRecord
import datetime
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse


# Create your views here.


def sayHello(request):
    return render(request, 'Login.html')


def loginPage(request):
    return render(request, 'Login.html')


def login(request):
    try:
        employee = Employees.objects.get(employeeId=request.GET.get('employeeId'))
        if employee.employeePwd == request.GET.get('loginPwd'):
            return JsonResponse(
                {'respCode': '1000', 'respMsg': '成功', 'teamId': employee.teamId, 'teamName': employee.teamName})
        else:
            s = '密码错误'
            # html = '<html><head></head><body><h1> %s </h1></body></html>' % (s)
            return JsonResponse({'respCode': '1001', 'respMsg': s})
    except Exception as e:
        s = '暂无该用户信息'
        # html = '<html><head></head><body><h1> %s </h1></body></html>' % (s)
        return JsonResponse({'respCode': '2000', 'respMsg': s})


def show(request):
    temperatures = Temperatures.objects.all()
    temperatures = serializers.serialize("json", temperatures)
    return JsonResponse({'respCode': '1000', 'respMsg': '成功', 'temperatures': temperatures})


def TemperatureRecorder(request):
    return render(request, 'TemperatureRecorder.html')
