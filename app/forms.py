from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cama, Insumo, Material, Operario, Siembra, Cosecha, AspersionFertilizacion

class CamaForm(forms.ModelForm):
    class Meta:
        model = Cama
        fields = '__all__'

class SiembraForm(forms.ModelForm):
    operario = forms.ModelMultipleChoiceField(
                   widget = forms.CheckboxSelectMultiple,
                   queryset = Operario.objects.all()
           )

    class Meta:
        model = Siembra
        fields = "__all__"

        widgets = {
            'fecha_actividad': forms.DateInput(format=('%d/%m/%Y'),attrs={'class':'datepicker'}),
        }

class CosechaForm(forms.ModelForm):
    operario = forms.ModelMultipleChoiceField(
                   widget = forms.CheckboxSelectMultiple,
                   queryset = Operario.objects.all()
           )

    class Meta:
        model = Cosecha
        fields = "__all__"
        widgets = {
            'fecha_actividad': forms.DateInput(format=('%d/%m/%Y'),attrs={'class':'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super(CosechaForm, self).__init__(*args, **kwargs)
        self.fields['material'].queryset = Siembra.objects.none()

        if 'cama_actividad' in self.data:
            try:
                cama_id = self.data.get('cama_actividad')
                self.fields['material'].queryset = Siembra.objects.filter(cama_actividad = cama_id)
            except (ValueError, TypeError):
                pass  # invalid input
        elif self.instance.pk:
            self.fields['material'].queryset = self.instance.cama_actividad.siembra_set.order_by('fecha_actividad')

class AspersionFertilizacionForm(forms.ModelForm):
    operario = forms.ModelMultipleChoiceField(
                   widget = forms.CheckboxSelectMultiple,
                   queryset = Operario.objects.all()
           )
    
    class Meta:
        model = AspersionFertilizacion
        fields = '__all__'
        
class OperarioForm(forms.ModelForm):
    class Meta:
        model = Operario
        fields = '__all__'

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = "__all__"
        
class InsumoFormUpdate(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(InsumoFormUpdate, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
          self.fields['nombre_insumo'].widget.attrs['readonly'] = True

    def clean_foo_field(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
          return instance.nombre_insumo
        else:
          return self.cleaned_data['nombre_insumo']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = "__all__"

class MaterialFormUpdate(forms.ModelForm):
    class Meta:
        model = Material
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MaterialFormUpdate, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
          self.fields['nombre_material'].widget.attrs['readonly'] = True

    def clean_foo_field(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
          return instance.nombre_insumo
        else:
          return self.cleaned_data['nombre_material']

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True),
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='*Obligatorio')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

