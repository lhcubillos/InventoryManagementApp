from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime

import pytz




# Create your models here.
class Medicamento(models.Model):
    homeopatia = models.BooleanField(default=False)
    nombre_comercial = models.CharField(max_length=150,default="-")
    nombre_generico = models.CharField(max_length=150,default="-")
    cantidad_frasco = models.CharField(max_length=50,default="N/A")
    dosis = models.CharField(max_length=20,default="-")
    formato_medicamento = models.CharField(max_length=50,default="-")
    tipo_medicamento = models.CharField(max_length=100,default="-")
    descripcion = models.TextField(default="-")

    def __str__(self):
        return self.nombre_generico+" | "+self.nombre_comercial+" | Formato: "+self.formato_medicamento+" | "\
               +self.dosis+" | "+self.tipo_medicamento

# class Tipo_Ingreso(models.Model):
#     tipo = models.CharField(max_length=50)
#     def __str__(self):
#         return self.tipo
#
# class Tipo_Egreso(models.Model):
#     tipo = models.CharField(max_length=50)
#     def __str__(self):
#         return self.tipo

class Tipo_Orden(models.Model):
    tipo = models.CharField(max_length=50)
    clase = models.IntegerField()  # 0 ingreso, 1 traspaso, 2 egreso, 3 interno
    def __str__(self):
        return self.tipo

class Estacion(models.Model):
    estacion = models.CharField(max_length=100)
    def __str__(self):
        return self.estacion


# class Orden_Ingreso(models.Model):
#     medicamento = models.ForeignKey(Medicamento)
#     fecha_hora = models.DateTimeField(default=datetime.now)
#     cantidad = models.IntegerField()
#     tipo = models.ForeignKey(Tipo_Ingreso)
#     descripcion_tipo = models.CharField(max_length=150, blank=True, null=True,default="")
#     destino = models.ForeignKey(Estacion)
#     def __str__(self):
#         return str(self.fecha_hora)+": cant="+str(self.cantidad)+", med= "+str(self.medicamento) +\
#                ", tipo="+str(self.tipo)+", destino="+str(self.destino)
#
# class Orden_Salida(models.Model):
#     medicamento = models.ForeignKey(Medicamento)
#     fecha_hora = models.DateTimeField(default=datetime.now)
#     cantidad = models.IntegerField()
#     tipo = models.ForeignKey(Tipo_Egreso)
#     descripcion_tipo = models.CharField(max_length=150, blank=True, null=True, default="")
#     origen = models.ForeignKey(Estacion)
#     def __str__(self):
#         return str(self.fecha_hora)+": cant="+str(self.cantidad)+", med= "+str(self.medicamento) +\
#                ", tipo="+str(self.tipo)+", origen="+str(self.origen)

class Orden(models.Model):
    fecha_hora = models.DateTimeField(default=datetime.now)
    salida = models.BooleanField()
    tipo = models.ForeignKey(Tipo_Orden)
    descripcion_tipo = models.CharField(max_length=150, blank=True, null=True)
    origen = models.ForeignKey(Estacion,related_name="origen")
    destino = models.ForeignKey(Estacion, related_name="destino")
    user = models.ForeignKey(User)


    def __str__(self):
        return str(self.fecha_hora)+":  tipo="+str(self.tipo)+", origen="+str(self.origen)+\
               ", destino="+str(self.destino)+", user="+str(self.user)+", salida="+str(self.salida)

    @classmethod
    def create(cls, tipo,origen,destino,user,salida):
        orden = cls(tipo=tipo,origen=origen,destino=destino,user=user,salida=salida)
        # do something with the book
        return orden

class Ubicacion(models.Model):
    ubicacion = models.CharField(max_length=150)
    def __str__(self):
        return self.ubicacion

class Medicamento_Ubicacion(models.Model):
    medicamento = models.ForeignKey(Medicamento)
    ubicacion = models.ForeignKey(Ubicacion)
    def __str__(self):
        return "med=" + str(self.medicamento)+", ubicacion=" + str(self.ubicacion)

class Tipo_Usuario(models.Model):
    tipo = models.CharField(max_length=50)
    def __str__(self):
        return self.tipo



class Orden_Medicamento(models.Model):
    orden = models.ForeignKey(Orden)
    medicamento = models.ForeignKey(Medicamento)
    cantidad = models.IntegerField()
    fecha_vencimiento = models.DateField()
