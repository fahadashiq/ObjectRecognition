from django.db import models

from django.contrib.auth.models import User


class PredictedImage(models.Model):
    pic = models.FileField()
    prediction = models.CharField(max_length=200)
