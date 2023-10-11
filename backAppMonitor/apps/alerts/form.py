from django import forms
from .models import Alerts, EmailNotifications


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


class EmailAddForm(forms.ModelForm):
    class Meta:
        model = EmailNotifications
        fields = ["name", "email"]
        # Definimos clases de bostrap
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
          
        }

class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = EmailNotifications
        fields = ["name", "email"]
        # Definimos clases de bostrap
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
          
        }
