from django.urls import path, include
from rest_framework import routers
from .views import (
    EmpleadoViewSet, AmonestacionViewSet, AspiranteViewSet,
    EmpleadocapacitacionViewSet, EvaluacionViewSet, EvaluacioncriterioViewSet,
    AusenciaViewSet, ContratoViewSet, ConvocatoriaViewSet, DocumentoViewSet,
    EquipoViewSet, HistorialpuestoViewSet, IdiomaViewSet,
    InduccionViewSet, InducciondocumentoViewSet, PuestoViewSet, RolViewSet, 
    TerminacionlaboralViewSet, TipodocumentoViewSet, UsuarioViewSet, EstadoViewSet, 
    PuebloViewSet, CriterioViewSet, CapacitacionViewSet, PostulacionViewSet,
    VariableViewSet, SeguimientoVariableViewSet, SeguimientoViewSet, TipoevaluacionViewSet, limpiar_postulaciones, listar_convocatorias
)
from .viewspersonalizadas import  login_usuario  

from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'criterio', CriterioViewSet)
router.register(r'pueblocultura', PuebloViewSet)
router.register(r'empleados', EmpleadoViewSet)
router.register(r'amonestaciones', AmonestacionViewSet)
router.register(r'aspirantes', AspiranteViewSet)
router.register(r'empleadocapacitacion', EmpleadocapacitacionViewSet)
router.register(r'evaluacion', EvaluacionViewSet)
router.register(r'evaluacioncriterio', EvaluacioncriterioViewSet)
router.register(r'ausencias', AusenciaViewSet)
router.register(r'contratos', ContratoViewSet)
router.register(r'convocatorias', ConvocatoriaViewSet)
router.register(r'documentos', DocumentoViewSet)
router.register(r'equipos', EquipoViewSet)
router.register(r'historialpuestos', HistorialpuestoViewSet)
router.register(r'idiomas', IdiomaViewSet)
router.register(r'inducciones', InduccionViewSet)
router.register(r'inducciondocumentos', InducciondocumentoViewSet)
router.register(r'puestos', PuestoViewSet)
router.register(r'roles', RolViewSet)
router.register(r'terminacionlaboral', TerminacionlaboralViewSet)
router.register(r'tipodocumento', TipodocumentoViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'estados', EstadoViewSet)
router.register(r'capacitaciones', CapacitacionViewSet)
router.register(r'postulaciones', PostulacionViewSet)
router.register(r'variables', VariableViewSet)
router.register(r'seguimientovariable', SeguimientoVariableViewSet)
router.register(r'seguimientos', SeguimientoViewSet)
router.register(r'tipoevaluacion', TipoevaluacionViewSet)

urlpatterns = [
    path('', include(router.urls)),  
    path('login/', login_usuario),
    path('postulaciones/limpiar/<int:idconvocatoria>/', limpiar_postulaciones),
    path('convocatorias/', listar_convocatorias),   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
