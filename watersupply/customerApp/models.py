from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#create custom user
class CustomeUsers(AbstractUser):
    phone_number = models.BigIntegerField(null=True, blank=True, unique=True)
    address = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(null=True, blank=True, max_length=100)
    state = models.CharField(null=True, blank=True, max_length=50)
    country = models.CharField(null=True, blank=True, max_length=50)
    pincode = models.BigIntegerField(null=True, blank=True, max_length=6)
    
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'CustomeUsers'
