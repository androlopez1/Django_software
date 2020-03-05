from django.conf.urls import url

from . import views

from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

urlpatterns = [
##    url(r'^$', TemplateView.as_view(template_name='app/home.html'), name='home'),
    url(r'^$', views.home, name = 'home'),
    url(r'camas/$', views.lista_camas, name = 'lista_camas'),
    url(r'camas/add/$', views.CamaCreateView.as_view(), name = 'cama-add'),
    url(r'camas/(?P<id_modulo>.*\w+)/(?P<id_bloque>.*\w+)/(?P<id_cama>.*\w+)/$',
        views.cama_detail, name = 'cama_detail'),
    url(r'camas/update/(?P<pk>\d+)/$', views.CamaUpdateView.as_view(), name = 'cama_update'),
    url(r'camas/delete/(?P<pk>\d+)/$', views.CamaDeleteView.as_view(), name = 'cama_delete'),
    url(r'actividades/$',TemplateView.as_view(template_name='app/actividades.html'), name = 'lista_actividades'),
    #url(r'actividades/siembras$', views.lista_siembras, name = 'lista_siembras'),
    url(r'siembras/add/$', views.SiembraCreateView.as_view(), name = 'siembra-add'),
    url(r'actividades/siembras/(?P<pk>\d+)/$', views.siembra_detail,
        name = 'siembra_detail'),
    url(r'actividades/siembras/update/(?P<pk>\d+)/$', views.SiembraUpdateView.as_view(),
        name = 'siembra-update'),
    url(r'actividades/siembras/delete/(?P<pk>\d+)/$', views.SiembraDeleteView.as_view(),
        name = 'siembra_delete'),
    url(r'actividades/cosechas/$', views.lista_cosechas, name = 'lista_cosechas'),
    url(r'cosechas/add/$', views.CosechaCreateView.as_view(), name = 'cosecha-add'),
    url(r'actividades/cosechas/(?P<pk>\d+)/$', views.cosecha_detail,
        name = 'cosecha_detail'),
    url(r'actividades/cosechas/update/(?P<pk>\d+)/$', views.CosechaUpdateView.as_view(),
        name = 'cosecha-update'),
    url(r'actividades/cosechas/delete/(?P<pk>\d+)/$', views.CosechaDeleteView.as_view(),
        name = 'cosecha-delete'),
    url(r'actividades/fertilizaciones$', views.lista_fertilizaciones, name = 'lista_fertilizaciones'),
    url(r'fertilizaciones/add/$', views.FertilizacionCreateView.as_view(), name = 'fertilizacion-add'),
    url(r'actividades/fertilizaciones/(?P<pk>\d+)/$', views.fertilizacion_detail,
        name = 'fertilizacion_detail'),
    url(r'actividades/fertilizacion/update/(?P<pk>\d+)/$', views.FertilizacionUpdateView.as_view(),
        name = 'fertilizacion-update'),
    url(r'actividades/fertilizacion/delete/(?P<pk>\d+)/$', views.FertilizacionDeleteView.as_view(),
        name = 'fertilizacion_delete'),
    url(r'operarios/$', views.lista_operarios, name = 'lista_operarios'),
    url(r'operarios/add/$', views.OperarioCreateView.as_view(), name = 'operario-add'),
    url(r'operarios/update/(?P<pk>\d+)/$', views.OperarioUpdateView.as_view(),
        name = 'operario_update'),
    url(r'operarios/delete/(?P<pk>\d+)/$', views.OperarioDeleteView.as_view(),
        name = 'operario_delete'),
    url(r'insumos/$', views.lista_insumos, name = 'lista_insumos'),
    url(r'insumos/add/$', views.InsumoCreateView.as_view(), name = 'insumo-add'),
    url(r'insumos/update/(?P<pk>\d+)/$', views.InsumoUpdateView.as_view(),
        name = 'insumo_update'),
    url(r'insumos/delete/(?P<pk>\d+)/$', views.InsumoDeleteView.as_view(),
        name = 'insumo_delete'),
    url(r'materiales/$', views.lista_materiales, name = 'lista_materiales'),
    url(r'material/add/$', views.MaterialCreateView.as_view(), name = 'material-add'),
    url(r'materiales/update/(?P<pk>\d+)/$', views.MaterialUpdateView.as_view(),
        name = 'material_update'),
    url(r'materiales/delete/(?P<pk>\d+)/$', views.MaterialDeleteView.as_view(),
        name = 'material_delete'),
    url(r'lotes/$', views.lista_lotes, name = 'lista_lotes'),
    url(r'actividades/load-siembras/$', views.load_siembras_cama, name = 'load_siembras_cama'),
    url(r'actividades/siembras/filtro/$', views.FilteredSiembraListView.as_view(), name = "siembra_filter"),
]