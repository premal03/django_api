from django.db import models
from api_demo.signal import create_auth_token
# Create your models here.


class Students(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    rollno = models.IntegerField()
