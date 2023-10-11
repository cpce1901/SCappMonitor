from typing import Any, Dict
from django import forms
from .models import Alerts
from apps.sensors.models import Sensor


class AlertsAddForm(forms.ModelForm):
    class Meta:
        model = Alerts
        fields = ["type_name", "level", "limit", "status"]

        # Definimos clases de bostrap
        widgets = {
            "type_name": forms.Select(attrs={"class": "form-select"}),
            "level": forms.Select(attrs={"class": "form-select"}),
            "limit": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_limit(self):
        limit = self.cleaned_data["limit"]
        if limit < 0:
            raise forms.ValidationError("Debes ingresar un valor mayor a 0")

        return limit


class AlertsUpdateForm(forms.ModelForm):
    class Meta:
        model = Alerts
        fields = ["type_name", "level", "limit", "status"]

        # Definimos clases de bostrap
        widgets = {
            "type_name": forms.Select(attrs={"class": "form-select"}),
            "level": forms.Select(attrs={"class": "form-select"}),
            "limit": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
