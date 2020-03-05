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

from django.template import Context, loader
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import (Operario, Material, Insumo, Modulo, Bloque,
                     Siembra, Cosecha, Cama, AspersionFertilizacion)
from .forms import (CamaForm, InsumoForm, InsumoFormUpdate, MaterialForm,
                    MaterialFormUpdate,SiembraForm, OperarioForm, CosechaForm,
                    AspersionFertilizacionForm, SignUpForm)
from .tables import SiembraTable
import datetime
from datetime import date

# accounts
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

#filter tables
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .filters import *


def home(request):
    if request.user.is_authenticated:
        return render(request,'app/home.html')
        r
    else:
        return redirect('login')       

def lista_camas(request):
    if request.user.is_authenticated:
        lista_camas = Cama.objects.all().order_by("bloque__modulo__id_modulo")
        context = {
            'lista_camas': lista_camas,       
                   }
        return render(request, 'app/lista_camas.html', context)
    else:
        return redirect('login')


def cama_detail(request, id_modulo, id_bloque, id_cama ):
    if request.user.is_authenticated:
        cama = Cama.objects.get(id_cama = id_cama, bloque__id_bloque = id_bloque,
                                bloque__modulo__id_modulo = id_modulo)
        siembras_activas_cama = Siembra.objects.filter(cama_actividad__bloque__modulo__id_modulo = id_modulo,
                                                 cama_actividad__bloque__id_bloque = id_bloque,
                                                 cama_actividad__id_cama = id_cama, enable=True).order_by("-fecha_actividad")

        siembras_cama = Siembra.objects.filter(cama_actividad__bloque__modulo__id_modulo = id_modulo,
                                                 cama_actividad__bloque__id_bloque = id_bloque,
                                                 cama_actividad__id_cama = id_cama).order_by("-fecha_actividad")
        
        cosechas_cama = Cosecha.objects.filter(cama_actividad__bloque__modulo__id_modulo = id_modulo,
                                                 cama_actividad__bloque__id_bloque = id_bloque,
                                                 cama_actividad__id_cama = id_cama).order_by("-fecha_actividad")

        actividades_cama = AspersionFertilizacion.objects.filter(cama_actividad__bloque__modulo__id_modulo = id_modulo,
                                                 cama_actividad__bloque__id_bloque = id_bloque,
                                                 cama_actividad__id_cama = id_cama).order_by('-fecha_actividad')
        context = {
            'siembras_activas_cama' : siembras_activas_cama,
            'siembras_cama' : siembras_cama,
            'cosechas_cama' : cosechas_cama,
            'actividades_cama': actividades_cama,
            'cama' : cama,
                   }
        return render(request, 'app/cama_detail.html', context)
    else:
        return redirect('login') 

class CamaCreateView(CreateView):
    model = Cama
    form_class = CamaForm
    success_url = reverse_lazy('lista_camas')

class CamaUpdateView(UpdateView):
    model = Cama
    form_class = CamaForm
    success_url = reverse_lazy('lista_camas')

class CamaDeleteView(DeleteView):
    model = Cama
    success_url = reverse_lazy('lista_camas')

# def lista_siembras(request):
#     if request.user.is_authenticated:
#         siembras = Siembra.objects.all().order_by("-fecha_actividad")
#         page = request.GET.get('page', 1)
#         paginator = Paginator(siembras, 20)
#         try:
#             lista_siembras= paginator.page(page)
#         except PageNotAnInteger:
#             lista_siembras = paginator.page(1)
#         except EmptyPage:
#             lista_siembras = paginator.page(paginator.num_pages)
#         context = {
#             'lista_siembras': lista_siembras,
#                    }
#         return render(request, 'app/lista_siembras.html', context)

class FilteredSiembraListView(SingleTableMixin, FilterView):
    table_class = SiembraTable
    model = Siembra
    template_name = "siembra_filter.html"

    filterset_class = SiembraFilter


def siembra_detail(request, pk):
    if request.user.is_authenticated:
        siembra = Siembra.objects.get(pk=pk)
        context = {
            'siembra' : siembra,
            }
        return render(request, 'app/siembra_detail.html', context)
    else:
        return redirect('login')

class SiembraCreateView(CreateView):
    model = Siembra
    form_class = SiembraForm
    success_url = reverse_lazy('lista_siembras')

class SiembraUpdateView(UpdateView):
    model = Siembra
    form_class = SiembraForm
    success_url = reverse_lazy('lista_siembras')

class SiembraDeleteView(DeleteView):
    model = Siembra
    success_url = reverse_lazy('lista_siembras')

def lista_cosechas(request):
    if request.user.is_authenticated:
        cosechas = Cosecha.objects.all().order_by("-fecha_actividad")
        page = request.GET.get('page', 1)
        paginator = Paginator(cosechas, 20)
        try:
            lista_cosechas= paginator.page(page)
        except PageNotAnInteger:
            lista_cosechas = paginator.page(1)
        except EmptyPage:
            lista_cosechas = paginator.page(paginator.num_pages)
        context = {
            'lista_cosechas': lista_cosechas,
                   }
        return render(request, 'app/lista_cosechas.html', context)
    else:
        return redirect('login')

def cosecha_detail(request, pk):
    if request.user.is_authenticated:
        cosecha = Cosecha.objects.get(pk=pk)
        context = {
            'cosecha' : cosecha,
            }
        return render(request, 'app/cosecha_detail.html', context)
    else:
        return redirect('login')
    
class CosechaCreateView(CreateView):
    model = Cosecha
    form_class = CosechaForm
    success_url = reverse_lazy('lista_cosechas')

    def form_valid(self, form):
        queda_producto = form.cleaned_data['queda_producto']
        material = form.cleaned_data['material']
        if queda_producto==False:
            siembra = Siembra.objects.get(pk=material.pk)
            siembra.enable = False
            siembra.save()
        elif queda_producto==True:
            siembra = Siembra.objects.get(pk=material.pk)
            siembra.enable = True
            siembra.save()
        form.save()
        template = loader.get_template("app/lista_actividades.html")
        return HttpResponse(template.render())
    

class CosechaUpdateView(UpdateView):
    model = Cosecha
    form_class = CosechaForm
    success_url = reverse_lazy('lista_cosechas')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        queda_producto = form.cleaned_data['queda_producto']
        material = form.cleaned_data['material']
        if queda_producto==False:
            siembra = Siembra.objects.get(pk=material.pk)
            siembra.enable = False
            siembra.save()
        elif queda_producto==True:
            siembra = Siembra.objects.get(pk=material.pk)
            siembra.enable = True
            siembra.save()
        self.object.save()
        template = loader.get_template("app/actividades.html")
        return HttpResponse(template.render())

class CosechaDeleteView(DeleteView):
    model = Cosecha
    success_url = reverse_lazy('lista_cosechas')

def lista_fertilizaciones(request):
    if request.user.is_authenticated:
        fertilizaciones = AspersionFertilizacion.objects.all().order_by("-fecha_actividad")
        page = request.GET.get('page', 1)
        paginator = Paginator(fertilizaciones, 5)
        try:
            lista_fertilizaciones= paginator.page(page)
        except PageNotAnInteger:
            lista_fertilizaciones = paginator.page(1)
        except EmptyPage:
            lista_fertilizaciones = paginator.page(paginator.num_pages)
        context = {
            'lista_fertilizaciones': lista_fertilizaciones,
                   }
        return render(request, 'app/lista_fertilizaciones.html', context)
    else:
        return redirect('login')


def fertilizacion_detail(request, pk):
    if request.user.is_authenticated:
        fertilizacion = AspersionFertilizacion.objects.get(pk=pk)
        context = {
            'fertilizacion' : fertilizacion,
            }
        return render(request, 'app/fertilizacion_detail.html', context)
    else:
        return redirect('login')

class FertilizacionCreateView(CreateView):
    model = AspersionFertilizacion
    form_class = AspersionFertilizacionForm
    success_url = reverse_lazy('lista_fertilizaciones')

class FertilizacionUpdateView(UpdateView):
    model = AspersionFertilizacion
    form_class = AspersionFertilizacionForm
    success_url = reverse_lazy('lista_fertilizaciones')

class FertilizacionDeleteView(DeleteView):
    model = AspersionFertilizacion
    success_url = reverse_lazy('lista_fertilizaciones')

def lista_operarios(request):
    if request.user.is_authenticated:
        operarios = Operario.objects.all().order_by("-codigo")
        page = request.GET.get('page', 1)
        paginator = Paginator(operarios, 10)
        try:
            lista_operarios= paginator.page(page)
        except PageNotAnInteger:
            lista_operarios = paginator.page(1)
        except EmptyPage:
            lista_operatios = paginator.page(paginator.num_pages)
        context = {
            'lista_operarios': lista_operarios,
                   }
        return render(request, 'app/lista_operarios.html', context)
    else:
        return redirect('login')

class OperarioCreateView(CreateView):
    model = Operario
    form_class = OperarioForm
    success_url = reverse_lazy('lista_operarios')

class OperarioUpdateView(UpdateView):
    model = Operario
    form_class = OperarioForm
    success_url = reverse_lazy('lista_operarios')

class OperarioDeleteView(DeleteView):
    model = Operario
    success_url = reverse_lazy('lista_operarios')


def lista_insumos(request):
    if request.user.is_authenticated:
        lista_insumos = Insumo.objects.all().order_by("nombre_insumo")
        context = {
            'lista_insumos': lista_insumos,       
                   }
        return render(request, 'app/lista_insumos.html', context)
    else:
        return redirect('login')

class InsumoCreateView(CreateView):
    model = Insumo
    form_class = InsumoForm
    success_url = reverse_lazy('lista_insumos')

class InsumoUpdateView(UpdateView):
    model = Insumo
    form_class = InsumoFormUpdate
    success_url = reverse_lazy('lista_insumos')

class InsumoDeleteView(DeleteView):
    model = Insumo
    success_url = reverse_lazy('lista_insumos')

def lista_materiales(request):
    if request.user.is_authenticated:
        lista_materiales = Material.objects.all().order_by("nombre_material")
        context = {
            'lista_materiales': lista_materiales,       
                   }
        return render(request, 'app/lista_materiales.html', context)
    else:
        return redirect('login')

class MaterialCreateView(CreateView):
    model = Material
    form_class = MaterialForm
    success_url = reverse_lazy('lista_materiales')

class MaterialUpdateView(UpdateView):
    model = Material
    form_class = MaterialFormUpdate
    success_url = reverse_lazy('lista_materiales')

class MaterialDeleteView(DeleteView):
    model = Material
    success_url = reverse_lazy('lista_materiales')

def load_siembras_cama(request):
    if request.user.is_authenticated:
        cama_id= request.GET.get('cama')
        siembras = Siembra.objects.filter(cama_actividad = cama_id, enable=True)
        return render(request, 'app/dropdown_list_options.html',
                      {'siembras': siembras})
    else:
        return redirect('login')

def lista_lotes(request):
    if request.user.is_authenticated:
        lotes = Cosecha.objects.all()
        context = {
            'lotes': lotes,       
                   }
        return render(request, 'app/lista_lotes.html', context)
    else:
        return redirect('login')

def signup(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
        else:
            form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})
    else:
        return redirect('login')

    
   
