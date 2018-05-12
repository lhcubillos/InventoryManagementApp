from django import forms
from .models import Orden, Orden_Medicamento, Tipo_Orden, Medicamento, Estacion

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import locale
locale.setlocale(locale.LC_TIME, '')


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
        dic["formato"] = med.formato_medicamento
        dic["tipo"] = med.tipo_medicamento
        dic["dosis"] = med.dosis
        dic["cantidad_bodega"] = value[0]
        dic["cantidad_botiquin"] = value[1]
        dic["fecha_venc"] = key[1]
        conteo_final.append(dic)
    return conteo_final


def try_parsing_date(text):
    # locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    for fmt in ("%b. %d, %Y", "%b %d, %Y","%B %d, %Y","%m/%Y"):
        try:
            print(fmt)
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError('no valid date format found')
