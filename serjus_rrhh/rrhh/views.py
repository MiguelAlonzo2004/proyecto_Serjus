from rest_framework import viewsets, status, filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
import os
from django.conf import settings
import shutil
from rest_framework.permissions import IsAuthenticated
from rrhh.authentication import BearerAuthentication
from rest_framework.permissions import AllowAny

from .models import (
    Empleado, Amonestacion, Aspirante,
    Empleadocapacitacion, Evaluacion, Evaluacioncriterio,
    Ausencia, Contrato, Convocatoria, Documento,
    Equipo, Historialpuesto, Idioma,
    Induccion, Inducciondocumento, Puesto, Rol,
    Terminacionlaboral, Tipodocumento, Usuario, Estado, Pueblocultura, Criterio, Capacitacion, Postulacion, Variable,
    Seguimientovariable, Seguimiento, Tipoevaluacion
)

from .serializers import (
    EmpleadoSerializer, AmonestacionSerializer, AspiranteSerializer,
    EmpleadocapacitacionSerializer, CapacitacionSerializer, EvaluacionSerializer, EvaluacioncriterioSerializer,
    AusenciaSerializer, ContratoSerializer, ConvocatoriaSerializer, DocumentoSerializer,
    EquipoSerializer, HistorialpuestoSerializer, IdiomaSerializer,
    InduccionSerializer, InducciondocumentoSerializer, PuestoSerializer, RolSerializer,
    TerminacionlaboralSerializer, TipodocumentoSerializer, UsuarioSerializer, EstadoSerializer, PuebloSerializer, CriterioSerializer,
    PostulacionSerializer, VariableSerializer, SeguimientoVariableSerializer, SeguimientoSerializer, TipoevaluacionSerializer
)

@extend_schema_view(
    list=extend_schema(tags=["Postulacion"]),
    retrieve=extend_schema(tags=["Postulacion"]),
    update=extend_schema(tags=["Postulacion"]),
    create=extend_schema(tags=["Postulacion"]),
)

class PostulacionViewSet(viewsets.ModelViewSet):
    queryset = Postulacion.objects.all()
    serializer_class = PostulacionSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        data = request.data
        if Postulacion.objects.filter(
            idaspirante=data.get("idaspirante"),
            idconvocatoria=data.get("idconvocatoria")
        ).exists():
            return Response(
                {"error": "El aspirante ya está postulado a esta convocatoria"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().create(request, *args, **kwargs)
    
@extend_schema_view(
    list=extend_schema(tags=["Aspirante"]),
    retrieve=extend_schema(tags=["Aspirante"]),
    update=extend_schema(tags=["Aspirante"]),
    create=extend_schema(tags=["Aspirante"]),
    destroy=extend_schema(tags=["Aspirante"]),
)
class AspiranteViewSet(viewsets.ModelViewSet):
    queryset = Aspirante.objects.all()
    serializer_class = AspiranteSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['dpi', 'nombreaspirante', 'apellidoaspirante']
    http_method_names = ['get', 'put', 'post', 'delete']  # ahora permite DELETE

    def destroy(self, request, *args, **kwargs):
        aspirante = self.get_object()
        aspirante_id = aspirante.idaspirante

        # Eliminar postulaciones del aspirante
        Postulacion.objects.filter(idaspirante=aspirante_id).delete()

        # 2Eliminar documentos asociados
        documentos = Documento.objects.filter(idaspirante=aspirante_id)
        for doc in documentos:
            # Eliminar archivo físico si existe
            if doc.archivo and os.path.exists(doc.archivo.path):
                os.remove(doc.archivo.path)
        documentos.delete()

        # Eliminar carpeta del aspirante
        aspirante_dir = os.path.join(settings.MEDIA_ROOT, f'documentos/aspirante_{aspirante_id}')
        if os.path.exists(aspirante_dir):
            shutil.rmtree(aspirante_dir, ignore_errors=True)

        # Eliminar aspirante
        aspirante.delete()

        return Response(
            {"message": f"Aspirante {aspirante_id} y todos sus datos fueron eliminados correctamente."},
            status=status.HTTP_204_NO_CONTENT
        )

@extend_schema_view(
    list=extend_schema(tags=["Criterio"]),
    retrieve=extend_schema(tags=["Criterio"]),
    update=extend_schema(tags=["Criterio"]),
    create=extend_schema(tags=["Criterio"]),
)
class CriterioViewSet(viewsets.ModelViewSet):
    queryset = Criterio.objects.all()
    serializer_class = CriterioSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']

@extend_schema_view(
    list=extend_schema(tags=["Pueblo y cultura"]),
    retrieve=extend_schema(tags=["Pueblo y cultura"]),
    update=extend_schema(tags=["Pueblo y cultura"]),
    create=extend_schema(tags=["Pueblo y cultura"]),
)
class PuebloViewSet(viewsets.ModelViewSet):
    queryset = Pueblocultura.objects.all()
    serializer_class = PuebloSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']

# ----------------- Recursos Humanos -----------------
@extend_schema_view(
    list=extend_schema(tags=["Empleado"]),
    retrieve=extend_schema(tags=["Empleado"]),
    update=extend_schema(tags=["Empleado"]),
    create=extend_schema(tags=["Empleado"]),
)
class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Amonestacion"]),
    retrieve=extend_schema(tags=["Amonestacion"]),
    update=extend_schema(tags=["Amonestacion"]),
    create=extend_schema(tags=["Amonestacion"]),
)
class AmonestacionViewSet(viewsets.ModelViewSet):
    queryset = Amonestacion.objects.all()
    serializer_class = AmonestacionSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Contrato"]),
    retrieve=extend_schema(tags=["Contrato"]),
    update=extend_schema(tags=["Contrato"]),
    create=extend_schema(tags=["Contrato"]),
)
class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Terminacionlaboral"]),
    retrieve=extend_schema(tags=["Terminacionlaboral"]),
    update=extend_schema(tags=["Terminacionlaboral"]),
    create=extend_schema(tags=["Terminacionlaboral"]),
)
class TerminacionlaboralViewSet(viewsets.ModelViewSet):
    queryset = Terminacionlaboral.objects.all()
    serializer_class = TerminacionlaboralSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Inactivar usuario vinculado al empleado
        empleado_id = request.data.get('idempleado')
        print(f"[DEBUG] idempleado recibido en terminación laboral: {empleado_id}")
        if empleado_id:
            from rrhh.models import Usuario, Empleado
            try:
                empleado = Empleado.objects.get(pk=empleado_id)
                print(f"[DEBUG] Empleado encontrado: {empleado}")
                usuarios = Usuario.objects.filter(idempleado=empleado)
                print(f"[DEBUG] Usuarios vinculados encontrados: {usuarios.count()}")
                for usuario in usuarios:
                    usuario.estado = False
                    usuario.save()
                    print(f"[DEBUG] Usuario inactivado: {usuario.idusuario}")
            except Empleado.DoesNotExist:
                print(f"[DEBUG] Empleado con id {empleado_id} no existe")
        else:
            print("[DEBUG] No se recibió idempleado en el request")
        return response


# ----------------- Capacitación y Evaluación -----------------
@extend_schema_view(
    list=extend_schema(tags=["Empleadocapacitacion"]),
    retrieve=extend_schema(tags=["Empleadocapacitacion"]),
    update=extend_schema(tags=["Empleadocapacitacion"]),
    create=extend_schema(tags=["Empleadocapacitacion"]),
)
class EmpleadocapacitacionViewSet(viewsets.ModelViewSet):
    queryset = Empleadocapacitacion.objects.all()
    serializer_class = EmpleadocapacitacionSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']

@extend_schema_view(
    list=extend_schema(tags=["Capacitacion"]),
    retrieve=extend_schema(tags=["Capacitacion"]),
    update=extend_schema(tags=["Capacitacion"]),
    create=extend_schema(tags=["Capacitacion"]),
)
class CapacitacionViewSet(viewsets.ModelViewSet):
    queryset = Capacitacion.objects.all()
    serializer_class = CapacitacionSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']

@extend_schema_view(
    list=extend_schema(tags=["Evaluacion"]),
    retrieve=extend_schema(tags=["Evaluacion"]),
    update=extend_schema(tags=["Evaluacion"]),
    create=extend_schema(tags=["Evaluacion"]),
)
class EvaluacionViewSet(viewsets.ModelViewSet):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Evaluacioncriterio"]),
    retrieve=extend_schema(tags=["Evaluacioncriterio"]),
    update=extend_schema(tags=["Evaluacioncriterio"]),
    create=extend_schema(tags=["Evaluacioncriterio"]),
)
class EvaluacioncriterioViewSet(viewsets.ModelViewSet):
    queryset = Evaluacioncriterio.objects.all()
    serializer_class = EvaluacioncriterioSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Induccion"]),
    retrieve=extend_schema(tags=["Induccion"]),
    update=extend_schema(tags=["Induccion"]),
    create=extend_schema(tags=["Induccion"]),
)
class InduccionViewSet(viewsets.ModelViewSet):
    queryset = Induccion.objects.all()
    serializer_class = InduccionSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Inducciondocumento"]),
    retrieve=extend_schema(tags=["Inducciondocumento"]),
    update=extend_schema(tags=["Inducciondocumento"]),
    create=extend_schema(tags=["Inducciondocumento"]),
)
class InducciondocumentoViewSet(viewsets.ModelViewSet):
    queryset = Inducciondocumento.objects.all()
    serializer_class = InducciondocumentoSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Seguimiento"]),
    retrieve=extend_schema(tags=["Seguimiento"]),
    update=extend_schema(tags=["Seguimiento"]),
    create=extend_schema(tags=["Seguimiento"]),
)
class SeguimientoViewSet(viewsets.ModelViewSet):
    queryset = Seguimiento.objects.all()
    serializer_class = SeguimientoSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Seguimientovariable"]),
    retrieve=extend_schema(tags=["Seguimientovariable"]),
    update=extend_schema(tags=["Seguimientovariable"]),
    create=extend_schema(tags=["Seguimientovariable"]),
)
class SeguimientoVariableViewSet(viewsets.ModelViewSet):
    queryset = Seguimientovariable.objects.all()
    serializer_class = SeguimientoVariableSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Tipoevaluacion"]),
    retrieve=extend_schema(tags=["Tipoevaluacion"]),
    update=extend_schema(tags=["Tipoevaluacion"]),
    create=extend_schema(tags=["Tipoevaluacion"]),
)    
class TipoevaluacionViewSet(viewsets.ModelViewSet):
    queryset = Tipoevaluacion.objects.all()
    serializer_class = TipoevaluacionSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


# ----------------- Administración -----------------
@extend_schema_view(
    list=extend_schema(tags=["Puesto"]),
    retrieve=extend_schema(tags=["Puesto"]),
    update=extend_schema(tags=["Puesto"]),
    create=extend_schema(tags=["Puesto"]),
)
class PuestoViewSet(viewsets.ModelViewSet):
    queryset = Puesto.objects.all()
    serializer_class = PuestoSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Rol"]),
    retrieve=extend_schema(tags=["Rol"]),
    update=extend_schema(tags=["Rol"]),
    create=extend_schema(tags=["Rol"]),
)
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Usuario"]),
    retrieve=extend_schema(tags=["Usuario"]),
    update=extend_schema(tags=["Usuario"]),
    create=extend_schema(tags=["Usuario"]),
)
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Estado"]),
    retrieve=extend_schema(tags=["Estado"]),
    update=extend_schema(tags=["Estado"]),
    create=extend_schema(tags=["Estado"]),
)
class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


# ----------------- Documentos -----------------
@extend_schema_view(
    list=extend_schema(tags=["Documento"]),
    retrieve=extend_schema(tags=["Documento"]),
    update=extend_schema(tags=["Documento"]),
    create=extend_schema(tags=["Documento"]),
)
class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Tipodocumento"]),
    retrieve=extend_schema(tags=["Tipodocumento"]),
    update=extend_schema(tags=["Tipodocumento"]),
    create=extend_schema(tags=["Tipodocumento"]),
)
class TipodocumentoViewSet(viewsets.ModelViewSet):
    queryset = Tipodocumento.objects.all()
    serializer_class = TipodocumentoSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


# ----------------- Otros -----------------
@extend_schema_view(
    list=extend_schema(tags=["Ausencia"]),
    retrieve=extend_schema(tags=["Ausencia"]),
    update=extend_schema(tags=["Ausencia"]),
    create=extend_schema(tags=["Ausencia"]),
)
class AusenciaViewSet(viewsets.ModelViewSet):
    queryset = Ausencia.objects.all()
    serializer_class = AusenciaSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Convocatoria"]),
    retrieve=extend_schema(tags=["Convocatoria"]),
    update=extend_schema(tags=["Convocatoria"]),
    create=extend_schema(tags=["Convocatoria"]),
)

class ConvocatoriaViewSet(viewsets.ModelViewSet):
    queryset = Convocatoria.objects.all()
    serializer_class = ConvocatoriaSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post', 'delete']


@extend_schema_view(
    list=extend_schema(tags=["Equipo"]),
    retrieve=extend_schema(tags=["Equipo"]),
    update=extend_schema(tags=["Equipo"]),
    create=extend_schema(tags=["Equipo"]),
)
class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Historialpuesto"]),
    retrieve=extend_schema(tags=["Historialpuesto"]),
    update=extend_schema(tags=["Historialpuesto"]),
    create=extend_schema(tags=["Historialpuesto"]),
)
class HistorialpuestoViewSet(viewsets.ModelViewSet):
    queryset = Historialpuesto.objects.all()
    serializer_class = HistorialpuestoSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']


@extend_schema_view(
    list=extend_schema(tags=["Idioma"]),
    retrieve=extend_schema(tags=["Idioma"]),
    update=extend_schema(tags=["Idioma"]),
    create=extend_schema(tags=["Idioma"]),
)
class IdiomaViewSet(viewsets.ModelViewSet):
    queryset = Idioma.objects.all()
    serializer_class = IdiomaSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']
    

@extend_schema_view(
    list=extend_schema(tags=["Variable"]),
    retrieve=extend_schema(tags=["Variable"]),
    update=extend_schema(tags=["Variable"]),
    create=extend_schema(tags=["Variable"]),
)
class VariableViewSet(viewsets.ModelViewSet):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer
    authentication_classes = [BearerAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'put', 'post']
    

@api_view(['PUT'])
def limpiar_postulaciones(request, idconvocatoria):
    # Nombres de estados que consideras como 'seleccionados'
    NOMBRES_SELECCIONADOS = ["Seleccionado para Entrevista"]

    # Obtener los IDs de esos estados
    seleccion_ids = list(
        Estado.objects
        .filter(nombreestado__in=NOMBRES_SELECCIONADOS)
        .values_list('pk', flat=True)
    )

    # Buscar si hay postulaciones seleccionadas
    hay_seleccionadas = (
        Postulacion.objects
        .filter(idconvocatoria=idconvocatoria, idestado_id__in=seleccion_ids)
        .exists()
        if seleccion_ids else False
    )

    if hay_seleccionadas:
        return Response(
            {"error": "No se pueden limpiar las postulaciones: ya hay aspirantes seleccionados."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 🔹 Buscar el ID correspondiente al estado 'Rechazado'
    estado_rechazado = (
        Estado.objects
        .filter(nombreestado__iexact="Rechazado")
        .first()
    )

    if not estado_rechazado:
        return Response(
            {"error": "No se encontró el estado 'Rechazado' en la tabla Estado."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 🔹 Actualizar todas las postulaciones a inactivas y con estado 'Rechazado'
    actualizadas = (
        Postulacion.objects
        .filter(idconvocatoria=idconvocatoria)
        .update(estado=False, idestado=estado_rechazado.idestado)
    )

    return Response(
        {"mensaje": f"Se marcaron {actualizadas} postulaciones como inactivas y rechazadas."},
        status=status.HTTP_200_OK
    )



#Cerrar convocatoria al vencer
@api_view(['GET'])
def listar_convocatorias(request):
    hoy = timezone.now().date()

    # Actualizar todas las que ya vencieron
    vencidas = Convocatoria.objects.filter(fechafin__lt=hoy, estado=True)
    for conv in vencidas:
        conv.actualizar_estado_automatico()

    convocatorias = Convocatoria.objects.all().order_by('-idconvocatoria')
    serializer = ConvocatoriaSerializer(convocatorias, many=True)
    return Response(serializer.data)