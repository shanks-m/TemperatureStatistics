from django.shortcuts import render
from TemperatureReporter.models import Employees, Temperatures, SubmitRecord
import datetime
from django.http import HttpResponse
# Create your views here.


def sayHello(request):
    return render(request, 'Login.html')


def login(request):
    try:
        employee = Employees.objects.get(employeeId=request.GET.get('employeeId'))
        if employee.employeePwd == request.GET.get('loginPwd'):
            return render(request, 'HelloWorld.html')
        else:
            s = '密码错误'
            html = '<html><head></head><body><h1> %s </h1></body></html>' % (s)
            return HttpResponse(html)
    except Exception as e:
        s = '暂无该用户信息'
        html = '<html><head></head><body><h1> %s </h1></body></html>' % (s)
        return HttpResponse(html)

