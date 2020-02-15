import json
import time

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from TemperatureReporter.forms import EmployeeTemperatureSubmitForm, GetEmployeeTemperatureForm
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


def getEmployeeTemperatureByTeamId(request):
    respJson = {'respCode': '1000', 'respMsg': '提交成功'}

    # 不支持get
    if not request.method == 'POST':
        respJson['respCode'] = '1001'
        respJson['respMsg'] = '系统异常[TR-1001]'
        return JsonResponse(respJson)

    form = GetEmployeeTemperatureForm(request.POST)

    # 参数不合法（是否必传 长度是否合法）
    if not form.is_valid():
        respJson['respCode'] = '1002'
        respJson['respMsg'] = '参数不合法[TR-1002]'
        return JsonResponse(respJson)

    # sessionId = form.cleaned_data['sessionId']
    teamId = form.cleaned_data['teamId']
    measureTimes = form.cleaned_data['measureTimes']  # 测量第次
    # date = form.cleaned_data['date']

    try:
        # 根据teamId获取员工列表
        employees = Employees.objects.filter(teamId=teamId)
        # employeeIdList = serializers.serialize("json", employeeIdList)
        # if not employeeIdList.exists():
        #     respJson['respCode'] = '1003'
        #     respJson['respMsg'] = '小组不存在[TR-1003]'
        #     return HttpResponse(respJson)
        # respJson['employeeIdList'] = employeeIdList
        # recordList = []
        submitStatus = 1
        for employee in employees:
            employeeId = employee.employeeId
            print(employee.employeeId)
            temperatureRecords = Temperatures.objects.filter(employeeId=employeeId, measureTimes=measureTimes)
            respJson['submitStatus'] = submitStatus
            temperatureRecords = serializers.serialize("json", temperatureRecords)
            respJson['recordList'] = temperatureRecords
        return JsonResponse(respJson)
    except Exception as e:
        print(e)
        respJson['respCode'] = '2000'
        respJson['respMsg'] = '系统异常[TR-2000]'
        return JsonResponse(respJson)

    # try:
    #
    # except Exception as e:  # 异常
    #     respJson['respCode'] = '2000'
    #     respJson['respMsg'] = '系统异常[TR-2000]'
    #     return HttpResponse(json.dumps(respJson))
    # temperatures = Temperatures.objects.all()
    # temperatures = serializers.serialize("json", temperatures)
    # return JsonResponse({'respCode': '1000', 'respMsg': '成功', 'temperatures': temperatures})


def TemperatureRecorder(request):
    return render(request, 'TemperatureRecorder.html')


# 员工体温数据提交测试页
def employeeSubmitTest(request):
    return render(request, 'EmployeeSubmitTest.html')


# 员工体温数据提交接口
def employeeTemperatureSubmit(request):
    respJson = {}
    respJson['respCode'] = '1000'
    respJson['respMsg'] = '提交成功'

    # 不支持get
    if not request.method == 'POST':
        respJson['respCode'] = '1001'
        respJson['respMsg'] = '系统异常[TR-1001]'
        return HttpResponse(json.dumps(respJson))

    form = EmployeeTemperatureSubmitForm(request.POST)

    # 参数不合法（是否必传 长度是否合法）
    if not form.is_valid():
        respJson['respCode'] = '1002'
        respJson['respMsg'] = '参数不合法[TR-1002]'
        return HttpResponse(json.dumps(respJson))

    # sessionId = form.cleaned_data['sessionId']
    teamId = form.cleaned_data['teamId']
    employeeId = form.cleaned_data['employeeId']
    employeeName = form.cleaned_data['employeeName']
    temperature = form.cleaned_data['temperature']
    measureTimes = form.cleaned_data['measureTimes']  # 测量第次
    recorderId = form.cleaned_data['recorderId']
    recorderName = form.cleaned_data['recorderName']
    remark = form.cleaned_data['remark']

    try:
        # 1. 校验session

        # 2. 校验当前team当前第次是否已是提交状态，如已提交，则不可继续提交
        teamSubmitRecord = SubmitRecord.objects.filter(teamId=teamId, submitTimes=measureTimes,
                                                       submitDate=time.strftime('%Y-%m-%d',
                                                                                time.localtime(time.time())))
        if teamSubmitRecord.exists():
            respJson['respCode'] = '1003'
            respJson['respMsg'] = '小组记录已提交[TR-1003]'
            return HttpResponse(json.dumps(respJson))

        # 3. 校验记录员是否有记录体温权限
        # 暂时用employeeType字段判断是否是管理员，后期修改
        recorder = Employees.objects.filter(employeeId=recorderId, employeeType=1)
        if not recorder.exists():
            respJson['respCode'] = '1004'
            respJson['respMsg'] = '当前操作员无记录权限[TR-1004]'
            return HttpResponse(json.dumps(respJson))

        # 4. 检查当前员工是否存在
        employee = Employees.objects.filter(employeeId=employeeId)
        if not employee.exists():
            respJson['respCode'] = '1005'
            respJson['respMsg'] = '该员工不存在[TR-1005]'
            return HttpResponse(json.dumps(respJson))

        # 5. 检查库中是否已经存在记录，如已存在，则执行update；不存在，则insert
        employeeSubmitRecord = Temperatures.objects.filter(employeeId=employeeId, measureTimes=measureTimes,
                                                           measureDate=time.strftime('%Y-%m-%d',
                                                                                     time.localtime(
                                                                                         time.time())))
        if employeeSubmitRecord.exists():
            # update操作
            Temperatures.objects.filter(employeeId=employeeId, measureTimes=measureTimes,
                                        measureDate=time.strftime('%Y-%m-%d', time.localtime(time.time()))).update(
                recorderId=recorderId,
                recorderName=recorderName,
                remark=remark,
                temperature=temperature,
                updatedAt=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        else:
            # insert操作
            Temperatures.objects.create(employeeId=employeeId, employeeName=employeeName,
                                        measureDate=time.strftime('%Y-%m-%d', time.localtime(time.time())),
                                        measureTimes=measureTimes,
                                        temperature=temperature,
                                        createdAt=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                        updatedAt=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                        recorderId=recorderId, recorderName=recorderName, remark=remark)

        return HttpResponse(json.dumps(respJson))

    except Exception as e:  # 异常
        respJson['respCode'] = '2000'
        respJson['respMsg'] = '系统异常[TR-2000]'
        return HttpResponse(json.dumps(respJson))
