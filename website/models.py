from django.db import models

# Create your models here.

class Patient(models.Model):
    NRIC = models.CharField(max_length=9)
    Name = models.CharField(max_length=100)
    Phone = models.IntegerField(unique=True)
    Email = models.EmailField(unique=True)