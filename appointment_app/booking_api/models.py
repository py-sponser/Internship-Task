from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import phonenumber_field.formfields

# Create your models here.
class AppointmentRequests(models.Model):
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    email_address = models.EmailField(null=True)
    phone_number = PhoneNumberField(null=True)
    countries = models.TextField()
    company = models.CharField(max_length=255,null=True)
    objective = models.CharField(max_length=255)
    details = models.TextField()
    completed = models.BooleanField(default=False)
    created_date = models.DateField(null=True,auto_now_add=True)