from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^panel/$', login_required(views.IndexView.as_view(),login_url="/"), name="panel"),
    url(r'^estadisticas/$', login_required(views.EstadisticasView.as_view(),login_url="/"), name="estadisticas"),
    url(r'^orden_ingreso/$', login_required(views.OrdenIngresoView.as_view(),login_url="/"), name="orden_ingreso"),
    url(r'^orden_egreso/$', login_required(views.OrdenEgresoView.as_view(),login_url="/"), name="orden_egreso"),
    url(r'^orden_traspaso/$', login_required(views.OrdenTraspasoView.as_view(),login_url="/"), name="orden_traspaso"),
    url(r'^chequeo_inventario/$', login_required(views.ChequeoInventarioView.as_view(),login_url="/"),
        name="chequeo_inventario"),
    url(r'^crear_medicamento/$', login_required(views.CrearMedicamentoView.as_view(),login_url="/"),
        name="crear_medicamento"),
]
