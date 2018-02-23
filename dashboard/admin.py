from django.contrib import admin
from .models import Medicamento,Orden,Tipo_Orden,Tipo_Usuario,User,Profile,Orden_Medicamento
# Register your models here.
admin.site.register(Medicamento)
admin.site.register(Orden)
admin.site.register(Tipo_Orden)
admin.site.register(Tipo_Usuario)
admin.site.register(Profile)
admin.site.register(Orden_Medicamento)
