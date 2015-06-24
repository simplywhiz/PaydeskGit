from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User)
    middle_name = models.CharField(max_length=50)
    membership_number = models.CharField(max_length=15)
    pin = models.SmallIntegerField()
    security_question = models.CharField(max_length=50)
    security_answer = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)

# Create your models here.
