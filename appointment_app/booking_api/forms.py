from django import forms
from .models import AppointmentRequests
from appointment_app import settings
class AppointmentUpdate(forms.ModelForm):
    class Meta:
        model = AppointmentRequests
        exclude = ["created_date",]