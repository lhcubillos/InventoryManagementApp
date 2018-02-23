from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import LoginForm,OrdenIngresoForm,OrdenMedicamentoForm
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import render
from .models import Medicamento,Tipo_Orden,Estacion,Orden,Orden_Medicamento

from datetime import datetime

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
            if orden.origen.estacion == "Botiquín":
                conteo_medicamentos[(med.id, fecha)][1] -= cant
            elif orden.origen.estacion == "Bodega":
                conteo_medicamentos[(med.id, fecha)][0] -= cant

            if orden.destino.estacion == "Botiquín":
                conteo_medicamentos[(med.id, fecha)][1] += cant
            elif orden.destino.estacion == "Bodega":
                conteo_medicamentos[(med.id, fecha)][0] += cant

    conteo_final = []
    for key, value in conteo_medicamentos.items():
        dic = {}
        med = Medicamento.objects.get(id=key[0])
        dic["generico"] = med.nombre_generico
        dic["comercial"] = med.nombre_comercial
        dic["cantidad_bodega"] = value[0]
        dic["cantidad_botiquin"] = value[1]
        dic["fecha_venc"] = key[1]
        conteo_final.append(dic)
    return conteo_final

class IndexView(TemplateView):
    template_name = "components/panel.html"


    def get_context_data(self, **kwargs):
        conteo_med1 = conteo_medicamentos()
        conteo_med = [x for x in conteo_med1 if x["fecha_venc"] < datetime.date(datetime.now())]
        por_fecha = sorted(conteo_med, key=lambda med: med["fecha_venc"])
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'title': "Panel","conteo":por_fecha,"total":conteo_med})
        return context



class BlankView(TemplateView):
    template_name = "components/blank.html"

    def get_context_data(self, **kwargs):
        context = super(BlankView, self).get_context_data(**kwargs)
        context.update({'title': "Blank Page"})
        return context


class ButtonsView(TemplateView):
    template_name = "components/buttons.html"

    def get_context_data(self, **kwargs):
        context = super(ButtonsView, self).get_context_data(**kwargs)
        context.update({'title': "Buttons"})
        return context


class FlotView(TemplateView):
    template_name = "components/flot.html"

    def get_context_data(self, **kwargs):
        context = super(FlotView, self).get_context_data(**kwargs)
        context.update({'title': "Flot Charts"})
        return context


class FormsView(TemplateView):
    template_name = "components/forms.html"

    def get_context_data(self, **kwargs):
        context = super(FormsView, self).get_context_data(**kwargs)
        context.update({'title': "Forms"})
        return context


class GridView(TemplateView):
    template_name = "components/grid.html"

    def get_context_data(self, **kwargs):
        context = super(GridView, self).get_context_data(**kwargs)
        context.update({'title': "Grid"})
        return context


class IconsView(TemplateView):
    template_name = "components/icons.html"

    def get_context_data(self, **kwargs):
        context = super(IconsView, self).get_context_data(**kwargs)
        context.update({'title': "Icons"})
        return context


class LoginView(TemplateView):
    template_name = "components/login.html"

    def get_context_data(self, **kwargs):
        form = LoginForm(self.request.POST)
        context = super(LoginView, self).get_context_data(**kwargs)
        context.update({'title': "Log In","form":form,"fallido":False})
        return context

    def post(self, request, *args, **kwargs):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user != None:
                login(request, user)
                return HttpResponseRedirect('/panel/')
            else:
                # the authentication system was unable to verify the username and password
                print("The username and password were incorrect.")
        else:
            form = LoginForm()
        return render(request, 'components/login.html', {'title': "Log In",'form': form,"fallido":True})

class LogoutView(RedirectView):
    pattern_name = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')

class MorrisView(TemplateView):
    template_name = "components/morris.html"

    def get_context_data(self, **kwargs):
        context = super(MorrisView, self).get_context_data(**kwargs)
        context.update({'title': "Morris Charts"})
        return context


class NotificationsView(TemplateView):
    template_name = "components/notifications.html"

    def get_context_data(self, **kwargs):
        context = super(NotificationsView, self).get_context_data(**kwargs)
        context.update({'title': "Notifications"})
        return context


class PanelsView(TemplateView):
    template_name = "components/panels-wells.html"

    def get_context_data(self, **kwargs):
        context = super(PanelsView, self).get_context_data(**kwargs)
        context.update({'title': "Panels and Wells"})
        return context


class TablesView(TemplateView):
    template_name = "components/tables.html"

    def get_context_data(self, **kwargs):
        context = super(TablesView, self).get_context_data(**kwargs)
        medicamentos = Medicamento.objects.values()
        context.update({'title': "Tables","medicamentos":medicamentos})
        return context


class TypographyView(TemplateView):
    template_name = "components/typography.html"

    def get_context_data(self, **kwargs):
        context = super(TypographyView, self).get_context_data(**kwargs)
        context.update({'title': "Typography"})
        return context

class OrdenIngresoView(TemplateView):
    template_name = "components/orden_ingreso.html"

    def get_context_data(self, **kwargs):
        #form = OrdenIngresoForm(self.request.POST)
        OrdenFormset = inlineformset_factory(Orden, Orden_Medicamento, form=OrdenMedicamentoForm,extra=1)
        context = super(OrdenIngresoView, self).get_context_data(**kwargs)
        tipos_orden = Tipo_Orden.objects.all()
        estaciones = Estacion.objects.all()
        medicamentos = Medicamento.objects.all()
        context.update({'title': "Orden Ingreso","formset":OrdenFormset(),
                        "fallido":False,"tipos":tipos_orden,"estaciones":estaciones,
                        "medicamentos":medicamentos})
        return context

    def post(self, request, *args, **kwargs):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user != None:
                login(request, user)
                return HttpResponseRedirect('/panel/')
            else:
                # the authentication system was unable to verify the username and password
                print("The username and password were incorrect.")
        else:
            form = LoginForm()
        return render(request, 'components/login.html', {'title': "Log In",'form': form,"fallido":True})

class OrdenEgresoView(TemplateView):
    template_name = "components/orden_egreso.html"

    formset_med = formset_factory(OrdenMedicamentoForm)

    def get_context_data(self, **kwargs):
        form = OrdenIngresoForm(self.request.POST)

        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': ''}
        med_formset = self.formset_med(data)
        context = super(OrdenEgresoView, self).get_context_data(**kwargs)
        tipos_orden = Tipo_Orden.objects.all()
        estaciones = Estacion.objects.all()
        medicamentos = Medicamento.objects.all()
        context.update({'title': "Orden Egreso", "formset": med_formset, "form_2": form,
                        "fallido": False, "tipos": tipos_orden, "estaciones": estaciones,
                        "medicamentos":medicamentos})
        return context

    def post(self, request, *args, **kwargs):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user != None:
                login(request, user)
                return HttpResponseRedirect('/panel/')
            else:
                # the authentication system was unable to verify the username and password
                print("The username and password were incorrect.")
        else:
            form = LoginForm()
        return render(request, 'components/login.html', {'title': "Log In", 'form': form, "fallido": True})

class EstadisticasView(TemplateView):
    template_name = "components/estadisticas.html"

    def get_context_data(self, **kwargs):
        context = super(EstadisticasView, self).get_context_data(**kwargs)
        context.update({'title': "Estadísticas"})
        return context

class ChequeoInventarioView(TemplateView):
    template_name = "components/chequeo_inventario.html"

    def get_context_data(self, **kwargs):
        conteo_final = conteo_medicamentos()
        context = super(ChequeoInventarioView, self).get_context_data(**kwargs)
        context.update({'title': "Chequeo Inventario","conteo":conteo_final})
        return context

