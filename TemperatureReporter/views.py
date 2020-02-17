import json
import time
import logging
import uuid
import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from TemperatureReporter.forms import EmployeeTemperatureSubmitForm, TeamTemperatureSubmitForm, \
    QueryTeamTemperatureRecordsForm
from TemperatureReporter.models import Employees, Temperatures, SubmitRecord, Session


# Create your views here.

def loginPage(request):
    return render(request, 'Login.html')


def login(request):
    # 不支持get
    if not request.method == 'POST':
        return JsonResponse({'respCode': '1001', 'respMsg': '系统异常[TR-1001]'})
    try:
        employee = Employees.objects.get(employeeId=request.POST.get('employeeId'))
        if employee.permission < 1:
            s = '抱歉，暂无权限'
            return JsonResponse({'respCode': '2000', 'respMsg': s})
        if employee.employeePwd == request.POST.get('loginPwd'):
            uid = str(uuid.uuid4())
            tmpid = ''.join(uid.split('-'))
            session = Session()
            session.createdAt = datetime.datetime.now()
            session.expireAt = session.createdAt + datetime.timedelta(minutes=60)
            session.sessionId = tmpid
            session.employeeId = employee.employeeId
            session.save()
            response = JsonResponse(
                {'respCode': '1000',
                 'respMsg': '成功',
                 'employeeId': employee.employeeId,
                 'teamId': employee.teamId,
                 'teamName': employee.teamName,
                 'sessionId': tmpid})
            response.set_cookie('sessionId', tmpid, expires=datetime.datetime.now() + datetime.timedelta(days=1),
                                path='/')
            response.set_cookie('employeeId', employee.employeeId,
                                expires=datetime.datetime.now() + datetime.timedelta(days=1), path='/')
            return response
        else:
            s = '密码错误'
            return JsonResponse({'respCode': '1001', 'respMsg': s})
    except Exception as e:
        s = '暂无该用户信息'
        return JsonResponse({'respCode': '2000', 'respMsg': s})


def TemperatureRecorder(request):
    employeeInfo = {'teamId': request.teamId,
                    'employeeId': request.employeeId,
                    'employeeName': request.employeeName,
                    'teamName': request.teamName}
    return render(request, 'TemperatureRecorder.html', {'employeeInfo': json.dumps(employeeInfo)})


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

    # 参数不合法（体温和备注不能同时为空）
    if not (temperature or remark):
        respJson['respCode'] = '1002'
        respJson['respMsg'] = '参数不合法[TR-1002]'
        return HttpResponse(json.dumps(respJson))

    try:
        # 1. 校验session

        # 2. 校验记录员是否有记录体温权限
        recorder = Employees.objects.filter(employeeId=recorderId, permission=1)
        if not recorder.exists():
            respJson['respCode'] = '1003'
            respJson['respMsg'] = '无操作权限[TR-1003]'
            return HttpResponse(json.dumps(respJson))

        # 3. 校验当前team当前第次是否已是提交状态，如已提交，则不可继续提交
        teamSubmitRecord = SubmitRecord.objects.filter(teamId=teamId, submitTimes=measureTimes,
                                                       submitDate=time.strftime('%Y-%m-%d',
                                                                                time.localtime(time.time())))
        if teamSubmitRecord.exists():
            respJson['respCode'] = '1004'
            respJson['respMsg'] = '小组记录已提交[TR-1004]'
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
            Temperatures.objects.create(employeeId=employeeId,
                                        employeeName=employeeName,
                                        measureDate=time.strftime('%Y-%m-%d', time.localtime(time.time())),
                                        measureTimes=measureTimes,
                                        temperature=temperature,
                                        createdAt=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                        updatedAt=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                        recorderId=recorderId,
                                        recorderName=recorderName,
                                        remark=remark)

        return HttpResponse(json.dumps(respJson))

    except Exception as e:  # 异常
        logger = logging.getLogger("console")
        logger.error("employeeTemperatureSubmit error", e)
        respJson['respCode'] = '2000'
        respJson['respMsg'] = '系统异常[TR-2000]'
        return HttpResponse(json.dumps(respJson))


# 小组体温数据提交接口
def teamTemperatureSubmit(request):
    respJson = {}
    respJson['respCode'] = '1000'
    respJson['respMsg'] = '提交成功'

    # 不支持get
    if not request.method == 'POST':
        respJson['respCode'] = '1001'
        respJson['respMsg'] = '系统异常[TR-1001]'
        return HttpResponse(json.dumps(respJson))

    form = TeamTemperatureSubmitForm(request.POST)

    # 参数不合法（是否必传 长度是否合法）
    if not form.is_valid():
        respJson['respCode'] = '1002'
        respJson['respMsg'] = '参数不合法[TR-1002]'
        return HttpResponse(json.dumps(respJson))

    # sessionId = form.cleaned_data['sessionId']
    teamId = form.cleaned_data['teamId']
    teamName = form.cleaned_data['teamName']
    recorderId = form.cleaned_data['recorderId']
    measureTimes = form.cleaned_data['measureTimes']  # 测量第次
    recorderName = form.cleaned_data['recorderName']

    try:
        # 1. 校验session

        # 2. 校验记录员是否有记录体温权限
        recorder = Employees.objects.filter(employeeId=recorderId, permission=1)
        if not recorder.exists():
            respJson['respCode'] = '1003'
            respJson['respMsg'] = '无操作权限[TR-1003]'
            return HttpResponse(json.dumps(respJson))

        # 3. 校验当前team当前第次是否已是提交状态，如已提交，则不可重复提交
        teamSubmitRecord = SubmitRecord.objects.filter(teamId=teamId, teamName=teamName, submitTimes=measureTimes,
                                                       submitDate=time.strftime('%Y-%m-%d',
                                                                                time.localtime(time.time())))
        if teamSubmitRecord.exists():
            respJson['respCode'] = '1004'
            respJson['respMsg'] = '小组记录已提交[TR-1004]'
            return HttpResponse(json.dumps(respJson))

        # 4 校验组内成员是否都已提交
        # 4.1 查找所有组成员
        teamMembers = Employees.objects.filter(teamId=teamId, teamName=teamName)
        if not teamMembers.exists():
            respJson['respCode'] = '1004'
            respJson['respMsg'] = '小组不存在[TR-1004]'
            return HttpResponse(json.dumps(respJson))

        # 4.2 查找当前日期 当前第次，员工体温记录是否都存在。都存在，且都合法，才可提交组数据。
        isValid = True
        try:
            for member in teamMembers:
                employeeSubmitRecord = Temperatures.objects.get(employeeId=member.employeeId,
                                                                measureTimes=measureTimes,
                                                                measureDate=time.strftime('%Y-%m-%d',
                                                                                          time.localtime(time.time())))
                if employeeSubmitRecord.temperature or employeeSubmitRecord.remark:
                    isValid = True
                else:
                    isValid = False
                    break

        except Exception as e:
            isValid = False

        if not isValid:
            respJson['respCode'] = '1005'
            respJson['respMsg'] = '请补全组内所有员工体温或备注信息后再提交[TR-1005]'
            respJson['submitStatus'] = 0
            return HttpResponse(json.dumps(respJson))

        # 5. 提交小组体温数据
        SubmitRecord.objects.create(teamId=teamId, teamName=teamName, recorderId=recorderId, recorderName=recorderName,
                                    submitTimes=measureTimes,
                                    submitDate=time.strftime('%Y-%m-%d', time.localtime(time.time())))
        respJson['submitStatus'] = 1
        return HttpResponse(json.dumps(respJson))

    except Exception as e:
        respJson['respCode'] = '2000'
        respJson['respMsg'] = '系统异常[TR-2000]'
        return HttpResponse(json.dumps(respJson))


# 小组体温查询接口
def queryTeamTemperatureRecords(request):
    respJson = {}
    respJson['respCode'] = '1000'
    respJson['respMsg'] = '成功'
    respJson['submitStatus'] = 0

    # 不支持get
    if not request.method == 'POST':
        respJson['respCode'] = '1001'
        respJson['respMsg'] = '系统异常[TR-1001]'
        return HttpResponse(json.dumps(respJson))

    form = QueryTeamTemperatureRecordsForm(request.POST)

    # 参数不合法（是否必传 长度是否合法）
    if not form.is_valid():
        respJson['respCode'] = '1002'
        respJson['respMsg'] = '参数不合法[TR-1002]'
        return HttpResponse(json.dumps(respJson))

    # sessionId = form.cleaned_data['sessionId']
    teamId = form.cleaned_data['teamId']
    recorderId = form.cleaned_data['recorderId']
    measureDate = form.cleaned_data['measureDate']
    measureTimes = form.cleaned_data['measureTimes']  # 测量第次

    # 日期默认为当前日期
    if not measureDate:
        measureDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    try:
        # 1. 校验session

        # 2. 校验记录员是否有记录体温权限
        recorder = Employees.objects.filter(employeeId=recorderId, permission=1)
        if not recorder.exists():
            respJson['respCode'] = '1003'
            respJson['respMsg'] = '无操作权限[TR-1003]'
            return HttpResponse(json.dumps(respJson))

        # 3. 校验小组是否存在
        teamMembers = Employees.objects.filter(teamId=teamId)
        if not teamMembers.exists():
            respJson['respCode'] = '1004'
            respJson['respMsg'] = '小组不存在[TR-1004]'
            return HttpResponse(json.dumps(respJson))

        # 4. 查询小组成员的体温记录
        hasRecordedMember = []
        notRecordedMember = []

        for member in teamMembers:
            dic = {}
            dic['employeeId'] = member.employeeId
            dic['employeeName'] = member.employeeName
            try:
                employeeSubmitRecord = Temperatures.objects.get(employeeId=member.employeeId,
                                                                measureTimes=measureTimes, measureDate=measureDate)
                dic['temperature'] = employeeSubmitRecord.temperature
                dic['recorderId'] = employeeSubmitRecord.recorderId
                dic['recorderName'] = employeeSubmitRecord.recorderName
                dic['remark'] = employeeSubmitRecord.remark
                hasRecordedMember.append(dic)
            except Exception as e:
                notRecordedMember.append(dic)
        respJson['recordList'] = notRecordedMember + hasRecordedMember  # 数据项排序

        # 5. 查询小组当前第次 当前时间提交状态
        teamSubmitRecord = SubmitRecord.objects.filter(teamId=teamId, submitTimes=measureTimes, submitDate=measureDate)
        if teamSubmitRecord.exists():
            respJson['submitStatus'] = 1

        return HttpResponse(json.dumps(respJson))

    except Exception as e:
        respJson['respCode'] = '2000'
        respJson['respMsg'] = '系统异常[TR-2000]'
        return HttpResponse(json.dumps(respJson))
