from django import forms
from .models import Orden,Orden_Medicamento,Tipo_Orden,Medicamento,Estacion


def conteo_medicamentos():
    a_contar = []
    ordenes = Orden.objects.all()
    ord_medicamentos = Orden_Medicamento.objects.all()
    for orden in ordenes:
        medicamentos = []
        for ord_med in ord_medicamentos:
            if ord_med.orden.id == orden.id:
                medicamentos.append((ord_med.medicamento, ord_med.cantidad, ord_med.fecha_vencimiento))
        a_contar.append((orden, medicamentos))
    conteo_medicamentos = {}  # id,fecha_vencimiento: [cantidad bodega,cantidad botiquín]
    for orden, meds in a_contar:
        for med, cant, fecha in meds:
            if (med.id, fecha) not in conteo_medicamentos.keys():
                conteo_medicamentos[(med.id, fecha)] = [0, 0]
            if orden.origen.estacion == "Botiquin":
                conteo_medicamentos[(med.id, fecha)][1] -= cant
            elif orden.origen.estacion == "Bodega":
                conteo_medicamentos[(med.id, fecha)][0] -= cant

            if orden.destino.estacion == "Botiquin":
                conteo_medicamentos[(med.id, fecha)][1] += cant
            elif orden.destino.estacion == "Bodega":
                conteo_medicamentos[(med.id, fecha)][0] += cant

    conteo_final = []
    for key, value in conteo_medicamentos.items():
        dic = {}
        med = Medicamento.objects.get(id=key[0])
        dic["id_med"] = key[0]
        dic["generico"] = med.nombre_generico
        dic["comercial"] = med.nombre_comercial
        dic["cantidad_bodega"] = value[0]
        dic["cantidad_botiquin"] = value[1]
        dic["fecha_venc"] = key[1]
        conteo_final.append(dic)
    return conteo_final

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
        fields = ['tipo','destino']

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
    def __init__(self,generico,comercial,fecha,cantidad_bodega,cantidad_botiquin,id_med):
        self.generico = generico
        self.comercial = comercial
        self.fecha = fecha
        self.cantidad_bodega = cantidad_bodega
        self.cantidad_botiquin = cantidad_botiquin
        self.id_med = id_med
    def __str__(self):
        return(str(self.id_med)+" | "+self.generico +" | " +self.comercial+" | Vence: "+str(self.fecha.strftime('%m/%Y'))+" | En Bodega: "+str(self.cantidad_bodega)+
        " | En Botiquín: "+str(self.cantidad_botiquin))


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
    obj = [MedFecha(c["generico"],c["comercial"],c["fecha_venc"],c["cantidad_bodega"],c["cantidad_botiquin"],c["id_med"]) for c in a]
    obj = sorted(obj,key=lambda x: (x.id_med,x.fecha))
    return [(o,str(o)) for o in obj]

def get_choices_traspaso():
    a = conteo_medicamentos()
    a = [b for b in a if b["cantidad_bodega"]>0]
    obj = [MedFecha(c["generico"],c["comercial"],c["fecha_venc"],c["cantidad_bodega"],c["cantidad_botiquin"],c["id_med"]) for c in a]
    obj = sorted(obj,key=lambda x: (x.id_med,x.fecha))
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