from django.db import models


# Create your models here.


class Temperatures(models.Model):
    id = models.AutoField(primary_key=True)
    employeeId = models.CharField(max_length=15)
    employeeName = models.CharField(max_length=50)
    measureDate = models.DateField()
    measureTimes = models.IntegerField()
    temperature = models.CharField(max_length=5)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    recorderId = models.CharField(max_length=15)
    recorderName = models.CharField(max_length=50)
    remark = models.CharField(max_length=512)


class Employees(models.Model):
    employeeId = models.CharField(primary_key=True, max_length=15)
    employeeName = models.CharField(max_length=50)
    employeePwd = models.CharField(max_length=15)
    teamId = models.CharField(max_length=50)
    teamName = models.CharField(max_length=50)
    employeeType = models.IntegerField()
    permission = models.IntegerField()


class SubmitRecord(models.Model):
    id = models.AutoField(primary_key=True)
    teamId = models.CharField(max_length=50)
    teamName = models.CharField(max_length=50)
    submitDate = models.DateField()
    submitTimes = models.IntegerField()


class Session(models.Model):
    sessionId = models.CharField(primary_key=True, max_length=50)
    employeeId = models.CharField(max_length=15)
    deviceId = models.CharField(max_length=50)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    expireAt = models.DateTimeField()
