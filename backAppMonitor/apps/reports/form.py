from django import forms

class GrupoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(GrupoForm, self).__init__(*args, **kwargs)

        vars_choices = [
            ("1", "Voltajes mono"),
            ("2", "Voltajes linea"),
            ("3", "Corrientes"),
            ("4", "Potencias"),
            ("5", "Energía"),
            ("6", "Factor de potencia"),
            ("7", "Frecuencia"),
        ]

        self.fields["grupo"] = forms.ChoiceField(
            label="Grupo de variables",
            choices=vars_choices,
            widget=forms.Select(
                attrs={
                    "id": "inputGroupSelect01",
                    "class": "form-select px-3",
                }
            ),
        )

        self.fields["date1"] = forms.DateTimeField(
            label="Desde",
            widget=forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        )

        self.fields["date2"] = forms.DateTimeField(
            label="Hasta",
            widget=forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        )
