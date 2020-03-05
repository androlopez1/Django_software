# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#from django.utils.encoding import smart_str, smart_unicode
from django.db import models
from app.choices import *
import datetime

class Operario(models.Model):
    nombre_operario = models.CharField(max_length=200)
    apellido_operario = models.CharField(max_length=200)
    cedula = models.IntegerField(blank=True, null=True)
    nacimiento = models.DateField('Fecha de Nacimiento',blank=True, null=True)
    codigo = models.CharField(max_length=200,blank=True, null=True)
    telefono = models.CharField(max_length=200, blank=True, null=True)
    inicio = models.DateField('Fecha de Inicio',blank=True, null=True)
    sexo = models.CharField(max_length=200, choices = OPCIONES_SEXO, default = GRAMOS,blank=True,
                              null=True)
    activo = models.NullBooleanField("Activo")
    
    def __str__(self):
        return '%s' % (str(self.codigo)) 
        
class Material(models.Model):
    nombre_material = models.CharField(max_length=200)
    variedad = models.CharField(max_length=200,blank=True, null=True)
    casa = models.CharField(max_length=200,blank=True, null=True)
    germinacion = models.FloatField("Germinacion (%)",default=None,blank=True, null=True)
    semillas_gramo = models.FloatField("Semillas por gramo",default=None,blank=True, null=True)

    def __str__(self):
        return self.nombre_material

class Insumo(models.Model):
    nombre_insumo = models.CharField('Nombre', max_length=200)
    fabricante = models.CharField(max_length=200,blank=True, null=True)
    variedad = models.CharField(max_length=200, choices = OPCIONES_INSUMO, default = CONTROL,
                                blank=True, null=True)
    cantidad = models.CharField(max_length=200,blank=True, null=True)
    unidad = models.CharField(max_length=200, choices = OPCIONES_UNIDAD, default = GRAMOS,blank=True,
                              null=True)
    dilucion = models.CharField(max_length=200,blank=True, null=True)
    def __str__(self):
        return self.nombre_insumo

class Modulo(models.Model):
    id_modulo = models.CharField(max_length=200)
    def __str__(self):
        return '%s %s' % (" Modulo ",str(self.id_modulo)) 

class Bloque(models.Model):
    modulo = models.ForeignKey(Modulo,on_delete=models.CASCADE)
    id_bloque = models.CharField(max_length=200)
    def __str__(self):
        return '%s %s' % (" Bloque ",str(self.id_bloque) +
                          " Modulo " + self.modulo.id_modulo) 

class Cama(models.Model):
    bloque = models.ForeignKey(Bloque, on_delete=models.CASCADE)
    id_cama = models.CharField(max_length=200)
    longitud = models.FloatField(default=None,blank=True, null=True)
    ancho = models.FloatField(default=None,blank=True, null=True)
    def __str__(self):
        return '%s %s' % (" Modulo " + self.bloque.modulo.id_modulo +
                          " Bloque " + self.bloque.id_bloque +
                          " Cama ", self.id_cama) 
    
class Siembra(models.Model):
    fecha_actividad = models.DateField('fecha (dd/mm/aaaa)', blank = True, null=True)
    operario = models.ManyToManyField(Operario)
    cama_actividad = models.ForeignKey(Cama, on_delete=models.CASCADE)
    cantidad = models.CharField(max_length=200,blank=True, null=True)
    unidad = models.CharField(max_length=200, choices = OPCIONES_UNIDAD, default = GRAMOS)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    enable = models.BooleanField("enable", default=True, editable=False)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s %s' % ("ID:" + str(self.pk) + " Fecha: " + str(self.fecha_actividad) +
                          str(self.cama_actividad) +
                          " Material " , self.material)
                            

class Cosecha(models.Model):
    fecha_actividad = models.DateField('fecha (dd/mm/aaaa)', default=datetime.date.today, blank=True, null=True)
    operario = models.ManyToManyField(Operario)
    cama_actividad = models.ForeignKey(Cama, on_delete=models.CASCADE)
    cantidad = models.CharField(max_length=200,blank=True, null=True)
    unidad = models.CharField(max_length=200, choices = OPCIONES_UNIDAD, default = GRAMOS)
    material = models.ForeignKey(Siembra,on_delete=models.CASCADE)
    queda_producto = models.BooleanField("Queda producto?", default=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s %s' % ("ID:" + str(self.pk) + " Fecha: " + str(self.fecha_actividad) +
                          str(self.cama_actividad) +
                          " Material: " , self.material.material)

class AspersionFertilizacion(models.Model):
    tipo = models.CharField(max_length=200, choices = OPCIONES_ACTIVIDAD, default = ASPERSION)
    fecha_actividad = models.DateField('fecha (dd/mm/aaaa)', default=datetime.date.today)
    operario = models.ManyToManyField(Operario)
    cama_actividad = models.ForeignKey(Cama, on_delete=models.CASCADE)
    cantidad = models.CharField(max_length=200,blank=True, null=True)
    unidad = models.CharField(max_length=200, choices = OPCIONES_UNIDAD, default = GRAMOS)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s %s' % ("ID:" + str(self.pk) +
                          " Tipo: " + str(self.tipo) +
                          " Fecha: " + str(self.fecha_actividad) +
                          str(self.cama_actividad) +
                          " Insumo " , self.insumo)

    class Meta:
        verbose_name = 'Otra actividad'
        verbose_name_plural = 'Otras actividades'
