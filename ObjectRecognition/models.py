from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User


# for uploaded images

class UploadedImage(models.Model):
    pic = models.FileField()
    perdiction = models.CharField(max_length=200)
    derived_perdiction = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('IdMain:voic', kwargs={'pk': self.pk})


class PredictedImage(models.Model):
    pic = models.FileField()
    prediction = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('IdMain:voic', kwargs={'pk': self.pk})
