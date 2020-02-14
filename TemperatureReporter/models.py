from django.db import models

# Create your models here.


class Temperatures(models.Model):
    id = models.AutoField(primary_key=True)
    employeeId = models.CharField(max_length=15)
    employeeName = models.CharField(max_length=15)
    measureDate = models.DateField()
    measureTimes = models.IntegerField()
    temperature = models.CharField(max_length=5)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    recorderId = models.CharField(max_length=15)
    recorderName = models.CharField(max_length=15)
    remark = models.CharField(max_length=512)


class Employees(models.Model):
    id = models.CharField(primary_key=True, max_length=15)
    name = models.CharField(max_length=15)
    pwd = models.CharField(max_length=15)
    teamId = models.CharField(max_length=15)
    teamName = models.CharField(max_length=15)


class SubmitRecord(models.Model):
    id = models.AutoField(primary_key=True)
    teamId = models.CharField(max_length=15)
    teamName = models.CharField(max_length=15)
    submitDate = models.DateField()
    submitTimes = models.IntegerField()
