import django_tables2 as tables
from .models import Siembra

class SiembraTable(tables.Table):
    class Meta:
        model = Siembra
        template_name = "django_tables2/bootstrap.html"
        fields = ("fecha_actividad", "cama_actividad", "material", "operario", 
        		 	"cantidad", "unidad", "observaciones")