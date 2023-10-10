from typing import Any, Dict
from django import forms
from .models import Alerts
from apps.sensors.models import Sensor


class AlertsAddForm(forms.ModelForm):
    class Meta:
        model = Alerts
        fields = ["type_name", "level", "limit", "status"]

    def clean_limit(self):
        limit = self.cleaned_data["limit"]
        if limit < 0:
            raise forms.ValidationError("Debes ingresar un valor mayor a 0")

        return limit



        

    
