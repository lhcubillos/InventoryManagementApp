from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


# Create your models here.
class Medicamento(models.Model):
    homeopatia = models.BooleanField(default=False)
    nombre_comercial = models.CharField(max_length=150,default="-")
    nombre_generico = models.CharField(max_length=150,default="-")
    cantidad_frasco = models.CharField(max_length=50,default="N/A")
    dosis = models.IntegerField(default=0)
    unidad_dosis = models.CharField(max_length=10,default="-")
    formato_medicamento = models.CharField(max_length=50,default="-")
    tipo_medicamento = models.CharField(max_length=100,default="-")
    descripcion = models.TextField(default="-")

    def __str__(self):
        return self.nombre_generico

class Tipo_Ingreso(models.Model):
    tipo = models.CharField(max_length=50)
    def __str__(self):
        return self.tipo

class Tipo_Egreso(models.Model):
    tipo = models.CharField(max_length=50)
    def __str__(self):
        return self.tipo

class Estacion(models.Model):
    estacion = models.CharField(max_length=100)
    clase = models.IntegerField() #0 ingreso, 1 traspaso, 2 egreso
    def __str__(self):
        return self.estacion

class Orden_Ingreso(models.Model):
    medicamento = models.ForeignKey(Medicamento)
    fecha_hora = models.DateTimeField(default=datetime.now)
    cantidad = models.IntegerField()
    tipo = models.ForeignKey(Tipo_Ingreso)
    descripcion_tipo = models.CharField(max_length=150, blank=True,default="")
    destino = models.ForeignKey(Estacion)
    def __str__(self):
        return str(self.fecha_hora)+": cant="+str(self.cantidad)+", med= "+str(self.medicamento) +\
               ", tipo="+str(self.tipo)+", destino="+str(self.destino)

class Orden_Salida(models.Model):
    medicamento = models.ForeignKey(Medicamento)
    fecha_hora = models.DateTimeField(default=datetime.now)
    cantidad = models.IntegerField()
    tipo = models.ForeignKey(Tipo_Egreso)
    descripcion_tipo = models.CharField(max_length=150, blank=True, default="")
    origen = models.ForeignKey(Estacion)
    def __str__(self):
        return str(self.fecha_hora)+": cant="+str(self.cantidad)+", med= "+str(self.medicamento) +\
               ", tipo="+str(self.tipo)+", origen="+str(self.origen)

class Ubicacion(models.Model):
    ubicacion = models.CharField(max_length=150)
    def __str__(self):
        return self.ubicacion

class Medicamento_Ubicacion(models.Model):
    medicamento = models.ForeignKey(Medicamento)
    ubicacion = models.ForeignKey(Ubicacion)
    def __str__(self):
        return "med=" + str(self.medicamento)+", ubicacion=" + str(self.ubicacion)



