from django import forms
from .models import Orden, Orden_Medicamento, Tipo_Orden, Medicamento, Estacion
from .methods import conteo_medicamentos


class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())

class OrdenIngresoForm(forms.ModelForm):
    tipo = forms.ModelChoiceField(queryset=Tipo_Orden.objects.filter(clase=0),
                                  widget=forms.widgets.Select(attrs={"class":"form-control",
                                                                     "id":"tipo-orden"}))
    destino = forms.ModelChoiceField(queryset=Estacion.objects.all().exclude(estacion="Otro"),
                                  widget=forms.widgets.Select(attrs={"class":"form-control"}))
    class Meta:
        def __init__(self, *args, **kwargs):
            self.fields['tipo'].label = "Tipo de Orden"
        model = Orden
        fields = ['tipo', 'destino']

class OrdenEgresoForm(forms.ModelForm):
    tipo = forms.ModelChoiceField(queryset=Tipo_Orden.objects.filter(clase=2).order_by('tipo')
                                  ,widget=forms.widgets.Select(attrs={"class":"form-control",
                                                                      "id": "tipo-orden"}))
    origen = forms.ModelChoiceField(queryset=Estacion.objects.all().exclude(estacion="Otro"),
                                     widget=forms.widgets.Select(attrs={"class": "form-control"}))
    class Meta:
        def __init__(self, *args, **kwargs):
            self.fields['tipo'].label = "Tipo de Orden"
        model = Orden
        fields = ['tipo','origen']

class MedFecha:
    def __init__(self, generico, comercial, fecha, cantidad_bodega,
                 cantidad_botiquin, id_med, dosis, formato):
        self.generico = generico
        self.comercial = comercial
        self.fecha = fecha
        self.cantidad_bodega = cantidad_bodega
        self.cantidad_botiquin = cantidad_botiquin
        self.id_med = id_med
        self.dosis = dosis
        self.formato = formato
    def __str__(self):
        return str(self.id_med)+" | "+self.generico+" | "+self.comercial+" | \
               Formato: "+self.formato + " | " + self.dosis + " | Vence: "\
               + str(self.fecha.strftime('%m/%Y'))+" | En Bodega: " +\
               str(self.cantidad_bodega) + " | En Botiquín: " +\
               str(self.cantidad_botiquin)


class OrdenMedicamentoForm(forms.ModelForm):

    class Meta:
        model = Orden_Medicamento

        fields = ['medicamento','cantidad','fecha_vencimiento']
        widgets = {"medicamento": forms.Select(attrs={"class": "form-control selectpicker",
                                                      "data-live-search":"true"}),
                   "cantidad":forms.NumberInput(attrs={"class": "form-control"})}

    fecha_vencimiento = forms.DateField(input_formats=["%m/%Y"],
        widget=forms.widgets.DateInput(format="%m/%Y",attrs={"class": "form-control"}))


def get_choices_egreso():
    a = conteo_medicamentos()
    a = [b for b in a if b["cantidad_bodega"]>0 or b["cantidad_botiquin"]>0]
    obj = [MedFecha(c["generico"],c["comercial"],c["fecha_venc"],
           c["cantidad_bodega"],c["cantidad_botiquin"],
           c["id_med"], c["dosis"], c["formato"]) for c in a]
    obj = sorted(obj,key=lambda x: (x.id_med, x.fecha))
    return [(o,str(o)) for o in obj]


def get_choices_traspaso():
    a = conteo_medicamentos()
    a = [b for b in a if b["cantidad_bodega"]>0]
    obj = [MedFecha(c["generico"],c["comercial"],c["fecha_venc"],
           c["cantidad_bodega"],c["cantidad_botiquin"],
           c["id_med"], c["dosis"], c["formato"]) for c in a]
    obj = sorted(obj, key=lambda x: (x.id_med,x.fecha))
    return [(o,str(o)) for o in obj]


class OrdenMedEgresoForm(forms.Form):

    medicamento = forms.ChoiceField(choices=get_choices_egreso(),widget=forms.widgets.Select(attrs={"class": "form-control selectpicker",
                                                                                   "data-live-search": "true"}))
    cantidad = forms.IntegerField(widget=forms.widgets.NumberInput(attrs={"class": "form-control"}))
    def __init__(self, *args, **kwargs):
        super(OrdenMedEgresoForm, self).__init__(*args, **kwargs)
        self.fields["medicamento"].choices = get_choices_egreso()


class OrdenMedTraspasoForm(forms.Form):

    medicamento = forms.ChoiceField(choices=get_choices_traspaso(),widget=forms.widgets.Select(attrs={"class": "form-control selectpicker",
                                                                                   "data-live-search": "true"}))
    cantidad = forms.IntegerField(widget=forms.widgets.NumberInput(attrs={"class": "form-control"}))
    def __init__(self, *args, **kwargs):
        super(OrdenMedTraspasoForm, self).__init__(*args, **kwargs)
        self.fields["medicamento"].choices = get_choices_traspaso()


class ChequeoBodegaForm(forms.Form):
    conteo_real_bodega = forms.IntegerField(widget=forms.widgets.NumberInput(attrs={"class": "form-control"}))

class ChequeoBotiquinForm(forms.Form):
    conteo_real_botiquin = forms.IntegerField(widget=forms.widgets.NumberInput(attrs={"class": "form-control"}))


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        exclude = []

    def __init__(self, *args, **kwargs):
        super(MedicamentoForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs\
                .update({
                    'class': 'form-control'
                })
