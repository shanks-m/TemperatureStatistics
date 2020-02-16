from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from TemperatureReporter.models import Session, Employees
import datetime

class sessionMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):

        # 统一验证登录
        # return None或者不写就不执行以后的操作
        if request.path == '/TemperatureReporter/' or request.path == '/TemperatureReporter/loginPage/' or request.path == '/TemperatureReporter/login/':
            return None

        sessionId = request.COOKIES.get('sessionId')
        employeeId = request.COOKIES.get('employeeId')

        if not sessionId:
            # 在浏览器中没有值返回登录页面
            return JsonResponse({'respMsg': '登录已过期，请重新登录', 'respCode': '7001'})

        try:
            session = Session.objects.get(sessionId=sessionId)
            if employeeId and employeeId != session.employeeId:
                return JsonResponse({'respMsg': '登录已过期，请重新登录', 'respCode': '7001'})
            if datetime.datetime.now() > session.expireAt:
                return JsonResponse({'respMsg': '登录已过期，请重新登录', 'respCode': '7001'})

            session.updatedAt = datetime.datetime.now()
            session.expireAt = session.updatedAt + datetime.timedelta(minutes=15)
            session.save()
        except Exception as e:
            return JsonResponse({'respMsg': '登录已过期，请重新登录', 'respCode': '7001'})
        # 登录信息都放这里面
        request.employeeId = session.employeeId
        employee = Employees.objects.get(employeeId=session.employeeId)
        request.teamId = employee.teamId
        request.teamName = employee.teamName
