from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import LoginForm,OrdenIngresoForm,OrdenMedicamentoForm,ChequeoBodegaForm,ChequeoBotiquinForm,\
    OrdenMedEgresoForm,OrdenEgresoForm,OrdenMedTraspasoForm
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import render
from .models import Medicamento,Tipo_Orden,Estacion,Orden,Orden_Medicamento

from datetime import datetime,date
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import locale
locale.setlocale(locale.LC_TIME, '')


def try_parsing_date(text):
    # locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    for fmt in ("%b. %d, %Y", "%b %d, %Y","%B %d, %Y","%m/%Y"):
        try:
            print(fmt)
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError('no valid date format found')

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

class IndexView(TemplateView):
    template_name = "components/panel.html"


    def get_context_data(self, **kwargs):
        conteo_med1 = conteo_medicamentos()
        conteo_med1 = [x for x in conteo_med1 if (x["cantidad_bodega"] > 0 or x["cantidad_botiquin"]>0) ]
        conteo_med = [x for x in conteo_med1 if x["fecha_venc"] < date.today() + relativedelta(months=+2) and
                      (x["cantidad_bodega"] > 0 or x["cantidad_botiquin"]>0)]

        por_fecha = sorted(conteo_med, key=lambda med: med["fecha_venc"])

        #(vencido,venciendose,remedio)
        por_fecha = [(True if x["fecha_venc"] < date.today() - relativedelta(months=+1)else False,
                      True if x["fecha_venc"] < date.today() else False,x) for x in por_fecha]
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'title': "Panel","conteo":por_fecha,"total":conteo_med1})
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

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect('/panel/')
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        # print(self.request.user.is_authenticated())

        form = LoginForm(self.request.POST)
        context = super(LoginView, self).get_context_data(**kwargs)
        context.update({'title': "Log In","form":form,"fallido":False})
        # if self.request.user != None:
        #     return HttpResponseRedirect('/panel/')

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
        return render(request, 'components/login.html', {'title': "Ingresar",'form': form,"fallido":True})

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
    OrdenFormset = formset_factory(OrdenMedicamentoForm, extra=1)
    def get_context_data(self, **kwargs):
        form = OrdenIngresoForm(self.request.POST)
        #OrdenFormset = inlineformset_factory(Orden, Orden_Medicamento, form=OrdenMedicamentoForm,extra=1)

        context = super(OrdenIngresoView, self).get_context_data(**kwargs)
        formset = self.OrdenFormset()
        context.update({'title': "Orden Ingreso","form2":form,"formset":formset})
        return context

    def post(self, request, *args, **kwargs):
        form = OrdenIngresoForm(self.request.POST)
        formset = self.OrdenFormset(self.request.POST)
        if all([form.is_valid(),formset.is_valid()]):
            desc_tipo = self.request.POST["desc_tipo"]
            nueva_orden = form.save(commit=False)
            nueva_orden.origen = Estacion.objects.filter(estacion="Otro")[0]
            nueva_orden.user = self.request.user
            nueva_orden.salida = False
            nueva_orden.descripcion_tipo = desc_tipo
            nueva_orden.save()

            for med_form in formset:
                nueva_med_orden = med_form.save(commit=False)
                nueva_med_orden.orden = nueva_orden
                nueva_med_orden.save()

            return HttpResponseRedirect('/panel/')

        else:
            print("no valido")
            print(formset.errors)
            form = OrdenIngresoForm()

        return HttpResponseRedirect('/orden_ingreso/')

class OrdenEgresoView(TemplateView):
    template_name = "components/orden_egreso.html"

    OrdenFormset = formset_factory(OrdenMedEgresoForm, extra=1)

    def get_context_data(self, **kwargs):
        form = OrdenEgresoForm(self.request.POST)
        # OrdenFormset = inlineformset_factory(Orden, Orden_Medicamento, form=OrdenMedicamentoForm,extra=1)

        context = super(OrdenEgresoView, self).get_context_data(**kwargs)
        formset = self.OrdenFormset()
        context.update({'title': "Orden Egreso", "form2": form, "formset": formset})
        return context

    def post(self, request, *args, **kwargs):
        form = OrdenEgresoForm(self.request.POST)
        formset = self.OrdenFormset(self.request.POST)
        if all([form.is_valid(), formset.is_valid()]):
            desc_tipo = self.request.POST["desc_tipo"]
            nueva_orden = form.save(commit=False)
            nueva_orden.destino = Estacion.objects.filter(estacion="Otro")[0]
            nueva_orden.user = self.request.user
            nueva_orden.salida = True
            nueva_orden.descripcion_tipo = desc_tipo
            nueva_orden.save()

            for med_form in formset:
                data = med_form.cleaned_data
                med = data.get("medicamento")
                id = int(med.split("|")[0])
                print(med.split("|")[3][-8:].strip())
                fecha = try_parsing_date(med.split("|")[3][-8:].strip()  )

                cantidad = data.get("cantidad")
                orden_med = Orden_Medicamento(orden=nueva_orden, medicamento=Medicamento.objects.get(id=id),
                                              fecha_vencimiento=fecha, cantidad=cantidad)
                orden_med.save()
            return HttpResponseRedirect('/panel/')

        else:
            print("no valido")
            print(formset.errors)
            form = OrdenEgresoForm()

        return HttpResponseRedirect('/orden_egreso/')

class OrdenTraspasoView(TemplateView):
    template_name = "components/orden_traspaso.html"

    OrdenFormset = formset_factory(OrdenMedTraspasoForm, extra=1)

    def get_context_data(self, **kwargs):
        # OrdenFormset = inlineformset_factory(Orden, Orden_Medicamento, form=OrdenMedicamentoForm,extra=1)

        context = super(OrdenTraspasoView, self).get_context_data(**kwargs)
        formset = self.OrdenFormset()
        context.update({'title': "Orden Traspaso", "formset": formset})
        return context

    def post(self, request, *args, **kwargs):
        formset = self.OrdenFormset(self.request.POST)
        if formset.is_valid():
            orden = Orden.create(Tipo_Orden.objects.get(tipo="Traspaso"),
                                 Estacion.objects.get(estacion="Bodega"),
                                 Estacion.objects.get(estacion="Botiquin"),
                                 request.user, False)
            orden.save()
            for med_form in formset:
                data = med_form.cleaned_data
                med = data.get("medicamento")
                id = int(med.split("|")[0])
                print(med.split("|")[3][-8:].strip())
                fecha = try_parsing_date(med.split("|")[3][-8:].strip()  )

                cantidad = data.get("cantidad")
                orden_med = Orden_Medicamento(orden=orden, medicamento=Medicamento.objects.get(id=id),
                                              fecha_vencimiento=fecha, cantidad=cantidad)
                orden_med.save()
            return HttpResponseRedirect('/panel/')

        else:
            print("no valido")
            print(formset.errors)
            form = OrdenEgresoForm()

        return HttpResponseRedirect('/orden_traspaso/')

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

        conteo_med1 = [x for x in conteo_final if (x["cantidad_bodega"] > 0 or x["cantidad_botiquin"] > 0)]

        por_generico = sorted(conteo_med1, key=lambda med: med["generico"])
        form_bodega = ChequeoBodegaForm()
        form_botiquin = ChequeoBotiquinForm()
        context = super(ChequeoInventarioView, self).get_context_data(**kwargs)
        context.update({'title': "Chequeo Inventario","conteo":por_generico,"form_bodega":form_bodega,
                        "form_botiquin":form_botiquin})
        return context

    def post(self, request, *args, **kwargs):
        if "act_botiquin" in request.POST:
            form_botiquin = ChequeoBotiquinForm(request.POST)
            if form_botiquin.is_valid():
                conteo_real = int(request.POST["conteo_real_botiquin"])
                id_med = request.POST["id_med"]
                fecha_venc = request.POST["fecha_venc"]
                f = "%b. %d, %Y"
                fecha_venc = try_parsing_date(fecha_venc)
                indice = int(request.POST["indice"])
                conteo_actual = conteo_medicamentos()
                orden = Orden.create(Tipo_Orden.objects.get(tipo="Ajuste"),
                                     Estacion.objects.get(estacion="Otro"),
                                     Estacion.objects.get(estacion="Botiquin"),
                                     request.user,False)
                orden.save()
                conteo_final = conteo_medicamentos()
                ajuste = conteo_real - conteo_final[indice]["cantidad_botiquin"]
                orden_med = Orden_Medicamento(orden=orden,medicamento=Medicamento.objects.get(id=id_med),
                                              fecha_vencimiento=fecha_venc,cantidad=ajuste)
                orden_med.save()
        elif "act_bodega" in request.POST:
            form_bodega = ChequeoBodegaForm(request.POST)
            if form_bodega.is_valid():
                conteo_real = int(request.POST["conteo_real_bodega"])
                id_med = request.POST["id_med"]
                fecha_venc = request.POST["fecha_venc"]
                fecha_venc = try_parsing_date(fecha_venc)
                print(fecha_venc)
                indice = int(request.POST["indice"])
                conteo_actual = conteo_medicamentos()
                orden = Orden.create(Tipo_Orden.objects.get(tipo="Ajuste"),
                                     Estacion.objects.get(estacion="Otro"),
                                     Estacion.objects.get(estacion="Bodega"),
                                     request.user, False)
                orden.save()
                conteo_final = conteo_medicamentos()
                ajuste = conteo_real - conteo_final[indice]["cantidad_bodega"]
                orden_med = Orden_Medicamento(orden=orden, medicamento=Medicamento.objects.get(id=id_med),
                                              fecha_vencimiento=fecha_venc, cantidad=ajuste)
                orden_med.save()

        return HttpResponseRedirect('/chequeo_inventario/')