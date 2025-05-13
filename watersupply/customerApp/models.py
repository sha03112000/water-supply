from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#create custom user
class CustomeUsers(AbstractUser):
    phone_number = models.BigIntegerField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.BigIntegerField(max_length=6)
    
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'CustomeUsers'
