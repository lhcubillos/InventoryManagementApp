from django import forms
from .models import Orden,Orden_Medicamento,Tipo_Orden

class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())

class OrdenIngresoForm(forms.ModelForm):
    class Meta:
        def __init__(self, *args, **kwargs):
            self.fields['tipo'].label = "Tipo de Orden"
        model = Orden
        fields = ['tipo','origen','destino']
        widgets = {"tipo":forms.Select(attrs={"class":"form-control"}),
                   "origen": forms.Select(attrs={"class": "form-control"}),
                   "destino":forms.Select(attrs={"class":"form-control"})}

class OrdenMedicamentoForm(forms.ModelForm):
    class Meta:
        model = Orden_Medicamento
        fields = ['medicamento','cantidad','fecha_vencimiento']
        widgets = {"medicamento": forms.Select(attrs={"class": "form-control"}),
                   "cantidad":forms.NumberInput(attrs={"class": "form-control"})}

    fecha_vencimiento = forms.DateField(input_formats=["%d/%m/%Y"],
        widget=forms.widgets.DateInput(format="%m/%Y",attrs={"class": "form-control"}))

class ChequeoInventarioForm(forms.Form):
    conteo_real_bodega = forms.IntegerField(widget=forms.widgets.NumberInput(attrs={"class": "form-control"}))
    conteo_real_botiquin = forms.IntegerField(widget=forms.widgets.NumberInput(attrs={"class": "form-control"}))