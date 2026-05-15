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
from .views import FormularioViewSet, FormularioRespuestaViewSet, PreguntaViewSet, OpcionViewSet, InduccionFormularioViewSet, EvaluacionGlobalViewSet
from .views import respuestas_por_induccion, detalle_respuesta, mi_respuesta, InformeCapacitacionViewSet, InformeCapacitacionDocumentoViewSet

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

##################################################################
#Formulario Induccion
router.register(r'formularios', FormularioViewSet)
router.register(r'formulario-respuestas', FormularioRespuestaViewSet)
router.register(r'preguntas', PreguntaViewSet)
router.register(r'opciones', OpcionViewSet)
router.register(r'induccion-formulario', InduccionFormularioViewSet)

##################################################################
#Evaluacion global
router.register(r'evaluacion-global', EvaluacionGlobalViewSet)

##################################################################
#Capacitaciones externas
router.register(
    r'informes-capacitacion',
    InformeCapacitacionViewSet,
    basename='informes-capacitacion'
)

router.register(
    r'informecapacitaciondocumento',
    InformeCapacitacionDocumentoViewSet
)

##########################################################################
#path's Custom
from .views import guardar_ficha_medica, ultima_ficha, guardar_encuesta_completa, obtener_encuesta_completa, guardar_registro_enfermedades, obtener_registro_enfermedades
from .views import estadisticas_enfermedades, obtener_evaluacion_periodo_prueba_acompanantes, obtener_evaluacion_periodo_prueba_coordinacion

urlpatterns = [
    path('', include(router.urls)),  
    path('login/', login_usuario),
    path('postulaciones/limpiar/<int:idconvocatoria>/', limpiar_postulaciones),
    path('convocatorias/', listar_convocatorias),   
    path('respuestas-induccion/<int:idinduccion>/', respuestas_por_induccion),
    path('detalle-respuesta/<int:idformulariorespuesta>/', detalle_respuesta),
    path('mi-respuesta/<int:idinduccion>/<int:idempleado>/', mi_respuesta),
    path('evaluacion-periodo-prueba-acompanantes', obtener_evaluacion_periodo_prueba_acompanantes),
    path('evaluacion-periodo-prueba-coordinacion',obtener_evaluacion_periodo_prueba_coordinacion),
    path('ficha-medica/', guardar_ficha_medica),
    path('ficha-medica/<int:idempleado>/', ultima_ficha),
    path('encuesta-completa/', guardar_encuesta_completa),
    path('encuesta-completa/<int:idempleado>/<int:idformulario>/', obtener_encuesta_completa),
    path('registro-enfermedades/', guardar_registro_enfermedades),
    path('registro-enfermedades/<int:idempleado>/', obtener_registro_enfermedades),
    path('estadisticas-enfermedades/', estadisticas_enfermedades),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
