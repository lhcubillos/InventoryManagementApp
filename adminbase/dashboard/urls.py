from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^index/$', login_required(views.IndexView.as_view(),login_url="/"), name="index"),
    url(r'^blank/$', login_required(views.BlankView.as_view(),login_url="/"), name="blank"),
    url(r'^buttons/$', login_required(views.ButtonsView.as_view(),login_url="/"), name="buttons"),
    url(r'^flot/$', login_required(views.FlotView.as_view(),login_url="/"), name="flot"),
    url(r'^forms/$', login_required(views.FormsView.as_view(),login_url="/"), name="forms"),
    url(r'^grid/$', login_required(views.GridView.as_view(),login_url="/"), name="grid"),
    url(r'^icons/$', login_required(views.IconsView.as_view(),login_url="/"), name="icons"),
    url(r'^morris/$', login_required(views.MorrisView.as_view(),login_url="/"), name="morris"),
    url(r'^notifications/$', login_required(views.NotificationsView.as_view(),login_url="/"), name="notifications"),
    url(r'^panels/$', login_required(views.PanelsView.as_view(),login_url="/"), name="panels"),
    url(r'^tables/$', login_required(views.TablesView.as_view(),login_url="/"), name="tables"),
    url(r'^typography/$', login_required(views.TypographyView.as_view(),login_url="/"), name="typography"),
]
