from django import forms
from .models import Orden,Orden_Medicamento

class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())

class OrdenIngresoForm(forms.ModelForm):
    class Meta:
        def __init__(self, *args, **kwargs):
            self.fields['tipo'].label = "Tipo de Orden"
        model = Orden
        fields = ['tipo','origen','destino']

class OrdenMedicamentoForm(forms.ModelForm):

    class Meta:
        model = Orden_Medicamento
        fields = ['medicamento','cantidad','fecha_vencimiento']