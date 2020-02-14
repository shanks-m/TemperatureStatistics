from django.db import models

# Create your models here.

class Temperatures(models.Model):
    id = models.AutoField(primary_key=True)
    employeeId = models.CharField(max_length=15)
    measureDate = models.DateField()
    measureTimes = models.IntegerField()
    temperature = models.CharField(max_length=5)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    recorderId = models.CharField(max_length=15)
    remark = models.CharField(max_length=512)
