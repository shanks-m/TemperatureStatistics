from django import forms


# 员工体温数据提交form
class EmployeeTemperatureSubmitForm(forms.Form):
    # sessionId = forms.CharField(max_length=30)
    teamId = forms.CharField(max_length=50)
    employeeId = forms.CharField(max_length=15)
    employeeName = forms.CharField(max_length=50)
    temperature = forms.CharField(max_length=5, required=False)
    measureTimes = forms.CharField(max_length=11)
    recorderId = forms.CharField(max_length=15)
    recorderName = forms.CharField(max_length=50)
    remark = forms.CharField(max_length=512, required=False)


# 员工体温记录获取form
class GetEmployeeTemperatureForm(forms.Form):
    # sessionId = forms.CharField(max_length=30)
    teamId = forms.CharField(max_length=50)
    measureTimes = forms.CharField(max_length=11)
    # date = forms.CharField(max_length=50)
