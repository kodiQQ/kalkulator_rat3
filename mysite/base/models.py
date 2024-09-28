
from django.db import models

# Create your models here.

class Wspolczynnik(models.Model):
    value = models.FloatField()
    def __str__(self):
        return str(self.value)