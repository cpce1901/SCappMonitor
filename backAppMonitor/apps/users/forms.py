from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuario",
                "id": "floatingInput",
                "class": "form-control px-5",
            }
        ),
    )

    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "id": "floatingPassword",
                "class": "form-control",
            }
        ),
    )


class UpdatePassForm(forms.Form):
    password1 = forms.CharField(
        label="Contraseña Actual",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña Actual",
                "id": "floatingPassword",
                "class": "form-control",
            }
        ),
    )

    password2 = forms.CharField(
        label="Nueva Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Nueva Contraseña",
                "id": "floatingPassword",
                "class": "form-control",
            }
        ),
    )
