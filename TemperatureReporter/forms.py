from django import forms


# 员工体温数据提交form
class EmployeeTemperatureSubmitForm(forms.Form):
    # sessionId = forms.CharField(max_length=30)
    teamId = forms.CharField(max_length=50)
    employeeId = forms.CharField(max_length=15)
    employeeName = forms.CharField(max_length=50, required=False)
    temperature = forms.CharField(max_length=5, required=False)
    measureTimes = forms.CharField(max_length=11)
    recorderId = forms.CharField(max_length=15)
    recorderName = forms.CharField(max_length=50, required=False)
    remark = forms.CharField(max_length=512, required=False)


class TeamTemperatureSubmitForm(forms.Form):
    # sessionId = forms.CharField(max_length=30)
    teamId = forms.CharField(max_length=50)
    teamName = forms.CharField(max_length=50)
    recorderId = forms.CharField(max_length=15)
    measureTimes = forms.CharField(max_length=11)
    recorderName = forms.CharField(max_length=50, required=False)


class QueryTeamTemperatureRecordsForm(forms.Form):
    # sessionId = forms.CharField(max_length=30)
    teamId = forms.CharField(max_length=50)
    recorderId = forms.CharField(max_length=15)
    measureDate = forms.CharField(required=False)
    measureTimes = forms.CharField(max_length=11)


