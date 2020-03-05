from .models import *
import django_filters

class SiembraFilter(django_filters.FilterSet):
    class Meta:
        model = Siembra
        fields = ("fecha_actividad", "cama_actividad", "material", "operario")