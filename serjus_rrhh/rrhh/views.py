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
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Max
from django.db import transaction
from datetime import datetime
from django.db.models import Count

from .models import (
    Empleado, Amonestacion, Aspirante,
    Empleadocapacitacion, Evaluacion, Evaluacioncriterio,
    Ausencia, Contrato, Convocatoria, Documento,
    Equipo, Historialpuesto, Idioma,
    Induccion, Inducciondocumento, Puesto, Rol,
    Terminacionlaboral, Tipodocumento, Usuario, Estado, Pueblocultura, Criterio, Capacitacion, Postulacion, Variable,
    Seguimientovariable, Seguimiento, Tipoevaluacion, InduccionFormulario, EnfermedadDetalle, RegistroEnfermedades, EvaluacionGlobal,
    InformeCapacitacionDocumento, InformeCapacitacion
)

from .serializers import (
    EmpleadoSerializer, AmonestacionSerializer, AspiranteSerializer,
    EmpleadocapacitacionSerializer, CapacitacionSerializer, EvaluacionSerializer, EvaluacioncriterioSerializer,
    AusenciaSerializer, ContratoSerializer, ConvocatoriaSerializer, DocumentoSerializer,
    EquipoSerializer, HistorialpuestoSerializer, IdiomaSerializer,
    InduccionSerializer, InducciondocumentoSerializer, PuestoSerializer, RolSerializer,
    TerminacionlaboralSerializer, TipodocumentoSerializer, UsuarioSerializer, EstadoSerializer, PuebloSerializer, CriterioSerializer,
    PostulacionSerializer, VariableSerializer, SeguimientoVariableSerializer, SeguimientoSerializer, TipoevaluacionSerializer, EvaluacionGlobalSerializer,
    InformeCapacitacionSerializer, InformeCapacitacionDocumentoSerializer
)

from .models import Formulario, Pregunta, Opcion, FormularioRespuesta, Respuesta

from .serializers import (
    FormularioSerializer,
    FormularioCreateSerializer,
    FormularioRespuestaSerializer,
    FormularioRespuestaCreateSerializer,
    RespuestaSerializer,
    PreguntaSerializer,
    OpcionSerializer,
    InduccionFormularioSerializer
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
        dpi = request.data.get("dpi")

        aspirante_existente = Aspirante.objects.filter(dpi=dpi).first()

        if aspirante_existente:
            # 🔄 OPCIÓN 1: actualizar datos
            serializer = self.get_serializer(
                aspirante_existente,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data, status=status.HTTP_200_OK)

        # 🆕 Si no existe, crear nuevo
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='por-dpi')
    def por_dpi(self, request):
        dpi = request.query_params.get("dpi")

        if not dpi:
            return Response({"error": "Debe enviar el DPI"}, status=400)

        aspirante = Aspirante.objects.filter(dpi=dpi).first()

        if not aspirante:
            return Response({"error": "Aspirante no encontrado"}, status=404)

        postulaciones = Postulacion.objects.filter(
            idaspirante=aspirante
        ).select_related("idconvocatoria", "idestado", "idconvocatoria__idpuesto")

        data = []
        for p in postulaciones:
            convocatoria = p.idconvocatoria
            estado = p.idestado

            data.append({
                "convocatoria": convocatoria.nombreconvocatoria if convocatoria else "",
                "puesto": (
                    convocatoria.idpuesto.nombrepuesto
                    if convocatoria and convocatoria.idpuesto else ""
                ),
                "fecha": p.fechapostulacion,
                "estado": estado.nombreestado if estado else ""
            })

        return Response({
            "aspirante": f"{aspirante.nombreaspirante} {aspirante.apellidoaspirante}",
            "dpi": aspirante.dpi,
            "postulaciones": data
        })
    
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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        estado_anterior = instance.estado
        response = super().update(request, *args, **kwargs)
        # Solo si el estado cambió de True a False (se inactiva)
        nuevo_estado = request.data.get('estado')
        if estado_anterior and (str(nuevo_estado).lower() in ['false', '0']):
            from django.utils import timezone
            from rrhh.models import Historialpuesto
            # Buscar el último historial de puesto del empleado
            ultimo_historial = Historialpuesto.objects.filter(idempleado=instance).order_by('-fechainicio').first()
            if ultimo_historial and not ultimo_historial.fechafin:
                # Si el campo es DateField, solo guardar la fecha
                fechafin_actual = timezone.now().date()
                ultimo_historial.fechafin = fechafin_actual
                ultimo_historial.save()
        return response


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

############################################################################
#Induccion Formulario
@extend_schema_view(
    list=extend_schema(tags=["Formulario"]),
    retrieve=extend_schema(tags=["Formulario"]),
    create=extend_schema(tags=["Formulario"]),
)
class FormularioViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch']
    queryset = Formulario.objects.all().order_by('-idformulario')
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FormularioCreateSerializer
        return FormularioSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # 🔥 AQUÍ ESTÁ EL DEBUG REAL
        if not serializer.is_valid():
            print("ERRORES DEL SERIALIZER:", serializer.errors)
            print("DATA QUE LLEGA:", request.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@extend_schema_view(
    list=extend_schema(tags=["Formulario Respuesta"]),
    retrieve=extend_schema(tags=["Formulario Respuesta"]),
    create=extend_schema(tags=["Formulario Respuesta"]),
)
class FormularioRespuestaViewSet(viewsets.ModelViewSet):
    queryset = FormularioRespuesta.objects.all().order_by('-idformulariorespuesta')
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        if self.action == 'create':
            return FormularioRespuestaCreateSerializer
        return FormularioRespuestaSerializer
    
    def create(self, request, *args, **kwargs):
        if not request.data.get("idempleado") and not request.data.get("idusuario"):
            return Response(
                {"error": "Debe enviar idempleado o idusuario"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='por-empleado')
    def por_empleado(self, request):
        idempleado = request.query_params.get('idempleado')

        if not idempleado:
            return Response({"error": "Debe enviar idempleado"}, status=400)

        respuestas = FormularioRespuesta.objects.filter(idempleado=idempleado)
        serializer = self.get_serializer(respuestas, many=True)

        return Response(serializer.data)
    
    @action(detail=True, methods=['put'], url_path='calificar')
    def calificar(self, request, pk=None):
        formulario_respuesta = self.get_object()
        respuestas = request.data.get('respuestas', [])
        total = 0

        for r in respuestas:
            respuesta = Respuesta.objects.get(idrespuesta=r.get('idrespuesta'))
            puntaje = r.get('puntaje', 0)
            comentario = r.get('comentario', '')

            respuesta.puntaje = puntaje
            respuesta.comentario = comentario
            respuesta.save()

            total += float(puntaje)

        formulario_respuesta.calificacion_total = total
        formulario_respuesta.revisado = True
        formulario_respuesta.save()

        return Response({
            "mensaje": "Formulario calificado correctamente",
            "total": total
        })
    
    @action(detail=True, methods=['get'], url_path='detalle')
    def detalle(self, request, pk=None):
        formulario_respuesta = self.get_object()
        serializer = FormularioRespuestaSerializer(formulario_respuesta)
        return Response(serializer.data)
    
class PreguntaViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer
    permission_classes = [AllowAny]

class OpcionViewSet(viewsets.ModelViewSet):
    queryset = Opcion.objects.all()
    serializer_class = OpcionSerializer
    permission_classes = [AllowAny]

class InduccionFormularioViewSet(viewsets.ModelViewSet):
    queryset = InduccionFormulario.objects.all()
    serializer_class = InduccionFormularioSerializer
    permission_classes = [AllowAny]

##########################################################
#Respuesta de Formularios
@api_view(['GET'])
def respuestas_por_induccion(request, idinduccion):

    respuestas = FormularioRespuesta.objects.filter(
        idformulario__induccionformulario__idinduccion=idinduccion,
        estado=True
    ).select_related('idempleado')

    data = []

    for fr in respuestas:
        empleado = fr.idempleado

        if not empleado:
            continue

        data.append({
            "idformulariorespuesta": fr.idformulariorespuesta,
            "idempleado": empleado.idempleado,
            "nombre": f"{empleado.nombre} {empleado.apellido}"
        })

    return Response(data)

@api_view(['GET'])
def detalle_respuesta(request, idformulariorespuesta):

    fr = get_object_or_404(FormularioRespuesta, pk=idformulariorespuesta)

    respuestas = fr.respuesta_set.select_related('idpregunta', 'idopcion')

    data = {
        "idformulariorespuesta": fr.idformulariorespuesta,
        "empleado": f"{fr.idempleado.nombre} {fr.idempleado.apellido}",
        "respuestas": []
    }

    for r in respuestas:
        data["respuestas"].append({
            "idrespuesta": r.idrespuesta,  # 👈 CLAVE
            "pregunta": r.idpregunta.texto,
            "respuesta": (
                r.respuesta_texto
                if r.respuesta_texto
                else r.idopcion.texto if r.idopcion else ""
            ),
            "comentario": r.comentario or ""  # 👈 opcional (para editar)
        })

    return Response(data)

@api_view(['GET'])
def mi_respuesta(request, idinduccion, idempleado):

    # 🔹 1. Buscar formulario asignado a la inducción
    asignacion = InduccionFormulario.objects.filter(
        idinduccion=idinduccion,
        estado=True
    ).first()

    if not asignacion:
        return Response({"error": "No hay formulario asignado"}, status=404)

    # 🔹 2. Buscar respuesta del empleado
    fr = FormularioRespuesta.objects.filter(
        idformulario=asignacion.idformulario,
        idempleado=idempleado
    ).first()

    if not fr:
        return Response({"error": "No ha respondido"}, status=404)

    respuestas = fr.respuesta_set.select_related('idpregunta', 'idopcion')

    data = {
        "idformulariorespuesta": fr.idformulariorespuesta,
        "respuestas": []
    }

    for r in respuestas:
        data["respuestas"].append({
            "pregunta": r.idpregunta.texto,
            "respuesta": r.respuesta_texto or (r.idopcion.texto if r.idopcion else ""),
            "comentario": r.comentario or ""
        })

    return Response(data)

###########################################################################################
#Periodo de Prueba
@api_view(['GET'])
def obtener_evaluacion_periodo_prueba_acompanantes(request):
    variables = Variable.objects.filter(
        idtipoevaluacion__nombretipo__iexact="Periodo de prueba acompañantes"
    ).prefetch_related('criterio_set')

    data = []

    for v in variables:
        criterios = v.criterio_set.filter(estado=True)  # 🔥 filtro importante

        data.append({
            "idvariable": v.idvariable,
            "nombrevariable": v.nombrevariable,
            "criterios": [
                {
                    "idcriterio": c.idcriterio,
                    "nombrecriterio": c.nombrecriterio
                }
                for c in criterios
            ]
        })
    
    print("VARIABLES:", variables.count())
    for v in variables:
        print("VAR:", v.nombrevariable, "CRITERIOS:", v.criterio_set.count())

    return Response(data)

@api_view(['GET'])
def obtener_evaluacion_periodo_prueba_coordinacion(request):

    variables = Variable.objects.filter(
        idtipoevaluacion__nombretipo__iexact="Periodo de prueba coordinaciones"
    ).prefetch_related('criterio_set')

    data = []

    for v in variables:

        criterios = v.criterio_set.filter(
            estado=True
        )

        data.append({
            "idvariable": v.idvariable,
            "nombrevariable": v.nombrevariable,

            "criterios": [
                {
                    "idcriterio": c.idcriterio,
                    "nombrecriterio": c.nombrecriterio
                }
                for c in criterios
            ]
        })

    print(
        "VARIABLES:",
        variables.count()
    )

    for v in variables:

        print(
            "VAR:",
            v.nombrevariable,
            "CRITERIOS:",
            v.criterio_set.count()
        )

    return Response(data)

##############################################################################
#Ficha Medica
from .models import FichaMedica, Empleado

@api_view(['POST'])
def guardar_ficha_medica(request):

    idempleado = request.data.get('idempleado')
    peso = request.data.get('peso')
    estatura = request.data.get('estatura')

    try:
        empleado = Empleado.objects.get(idempleado=idempleado)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no existe'}, status=404)

    ficha = FichaMedica.objects.create(
        idempleado=empleado,
        peso=peso,
        estatura=estatura
    )

    return Response({
        'mensaje': 'Ficha médica guardada',
        'idficha': ficha.idficha
    })

@api_view(['GET'])
def ultima_ficha(request, idempleado):

    ficha = FichaMedica.objects.filter(
        idempleado=idempleado
    ).order_by('-fecha_registro').first()

    if not ficha:
        return Response({'mensaje': 'Sin ficha'}, status=404)

    return Response({
        'peso': ficha.peso,
        'estatura': ficha.estatura
    })
    

@api_view(['POST'])
def guardar_encuesta_completa(request):

    try:
        with transaction.atomic():  # 🔥 TODO o NADA

            # 🔹 1. Obtener datos
            idempleado = request.data.get('idempleado')
            idformulario = request.data.get('idformulario')
            peso = request.data.get('peso')
            estatura = request.data.get('estatura')
            respuestas = request.data.get('respuestas', [])

            # 🔹 2. Validaciones básicas
            if not idempleado or not idformulario:
                return Response({'error': 'Faltan datos'}, status=400)

            if not isinstance(respuestas, list):
                return Response({'error': 'Formato de respuestas inválido'}, status=400)

            # 🔹 3. Obtener objetos
            empleado = Empleado.objects.get(idempleado=idempleado)
            formulario = Formulario.objects.get(idformulario=idformulario)

            # 🔥 4. VALIDACIÓN DE REGLAS DE NEGOCIO
            if formulario.tipo == 'induccion':

                existe = FormularioRespuesta.objects.filter(
                    idformulario=formulario,
                    idempleado=empleado
                ).exists()

                if existe:
                    return Response({
                        'error': 'Este formulario de inducción ya fue respondido'
                    }, status=400)

            elif formulario.tipo == 'medico':

                año_actual = datetime.now().year

                # 🔥 BORRAR SOLO LA DEL MISMO AÑO
                FormularioRespuesta.objects.filter(
                    idformulario=formulario,
                    idempleado=empleado,
                    fecha_respuesta__year=año_actual
                ).delete()

            # 🔥 5. GUARDAR FICHA MÉDICA
            if peso and estatura:
                FichaMedica.objects.create(
                    idempleado=empleado,
                    peso=peso,
                    estatura=estatura
                )

            # 🔥 6. CREAR FORMULARIO RESPUESTA
            formulario_respuesta = FormularioRespuesta.objects.create(
                idformulario=formulario,
                idempleado=empleado
            )

            # 🔥 7. GUARDAR RESPUESTAS
            for r in respuestas:

                pregunta = Pregunta.objects.get(idpregunta=r.get('idpregunta'))

                opcion = None
                if r.get('idopcion'):
                    opcion = Opcion.objects.get(idopcion=r.get('idopcion'))

                Respuesta.objects.create(
                    idformulariorespuesta=formulario_respuesta,
                    idpregunta=pregunta,
                    respuesta_texto=r.get('respuesta_texto'),
                    idopcion=opcion
                )

            return Response({
                'mensaje': 'Encuesta guardada correctamente',
                'idrespuesta': formulario_respuesta.idformulariorespuesta
            })

    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no existe'}, status=404)

    except Formulario.DoesNotExist:
        return Response({'error': 'Formulario no existe'}, status=404)

    except Pregunta.DoesNotExist:
        return Response({'error': 'Pregunta inválida'}, status=404)

    except Opcion.DoesNotExist:
        return Response({'error': 'Opción inválida'}, status=404)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def obtener_encuesta_completa(request, idempleado, idformulario):

    fr = FormularioRespuesta.objects.filter(
        idformulario_id=idformulario,
        idempleado_id=idempleado
    ).order_by('-fecha_respuesta').first()  # 🔥 SOLO LA ÚLTIMA

    if not fr:
        return Response([])

    respuestas = Respuesta.objects.filter(
        idformulariorespuesta=fr
    ).select_related('idopcion', 'idpregunta')

    data = []

    for r in respuestas:
        data.append({
            "idpregunta": r.idpregunta.idpregunta,
            "respuesta_texto": r.respuesta_texto,
            "idopcion": r.idopcion.idopcion if r.idopcion else None
        })

    return Response(data)

#######################################################################
#Registro de enfermedades
@api_view(['POST'])
def guardar_registro_enfermedades(request):

    try:
        with transaction.atomic():

            idempleado = request.data.get('idempleado')
            enfermedades = request.data.get('enfermedades', [])

            empleado = Empleado.objects.get(idempleado=idempleado)

            registro = RegistroEnfermedades.objects.create(
                idempleado=empleado,
                alergias=request.data.get('alergias', False),
                alergias_detalle=request.data.get('alergias_detalle', ''),
                operaciones=request.data.get('operaciones', False),
                operaciones_detalle=request.data.get('operaciones_detalle', ''),
                otras_enfermedades=request.data.get('otras', False),
                otras_detalle=request.data.get('otras_detalle', '')
            )

            for e in enfermedades:
                EnfermedadDetalle.objects.create(
                    registro=registro,
                    nombre=e.get('nombre'),
                    tiene=e.get('tiene'),
                    tiempo=e.get('tiempo'),
                    tratamiento=e.get('tratamiento')
                )

            return Response({"mensaje": "Guardado correctamente"})

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def obtener_registro_enfermedades(request, idempleado):
    try:
        año_actual = datetime.now().year

        registro = RegistroEnfermedades.objects.filter(
            idempleado=idempleado,
            fecha__year=año_actual
        ).order_by('-fecha').first()

        if not registro:
            return Response({"mensaje": "Sin registros"})

        detalles = EnfermedadDetalle.objects.filter(registro=registro)

        return Response({
            "alergias": registro.alergias,
            "alergias_detalle": registro.alergias_detalle,
            "operaciones": registro.operaciones,
            "operaciones_detalle": registro.operaciones_detalle,
            "otras": registro.otras_enfermedades,
            "otras_detalle": registro.otras_detalle,
            "enfermedades": [
                {
                    "nombre": d.nombre,
                    "tiene": d.tiene,
                    "tiempo": d.tiempo,
                    "tratamiento": d.tratamiento
                }
                for d in detalles
            ]
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['GET'])
def estadisticas_enfermedades(request):

    genero = request.query_params.get('genero')

    queryset = EnfermedadDetalle.objects.filter(
        tiene=True
    )

    # 🔥 aplicar filtro SOLO si viene género
    if genero and genero != "TODOS":
        queryset = queryset.filter(
            registro__idempleado__genero__istartswith=genero
        )

    data = (
        queryset
        .values('nombre')
        .annotate(
            total=Count('registro__idempleado', distinct=True)
        )
        .order_by('-total')
    )

    return Response(data)

#####################################################################
#Evaluacion Global
class EvaluacionGlobalViewSet(viewsets.ModelViewSet):
    queryset = EvaluacionGlobal.objects.all()
    serializer_class = EvaluacionGlobalSerializer

################################################################
#Informes de Capacitacion
class InformeCapacitacionViewSet(viewsets.ModelViewSet):

    queryset = InformeCapacitacion.objects.filter(
        estado=True
    ).order_by('-createdat')

    serializer_class = InformeCapacitacionSerializer

    @action(detail=True, methods=['post'], url_path='subir-documento')
    def subir_documento(self, request, pk=None):

        informe = self.get_object()

        iddocumento = request.data.get('iddocumento')

        if not iddocumento:
            return Response(
                {'error': 'iddocumento es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        documento = Documento.objects.filter(
            pk=iddocumento
        ).first()

        if not documento:
            return Response(
                {'error': 'Documento no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

        relacion = InformeCapacitacionDocumento.objects.create(
            idinformecapacitacion=informe,
            iddocumento=documento
        )

        serializer = InformeCapacitacionDocumentoSerializer(relacion)

        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='documentos')
    def documentos(self, request, pk=None):

        informe = self.get_object()

        documentos = informe.documentos.filter(
            estado=True
        )

        serializer = InformeCapacitacionDocumentoSerializer(
            documentos,
            many=True
        )

        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='capacitacion/(?P<idcapacitacion>[^/.]+)')
    def por_capacitacion(self, request, idcapacitacion=None):

        informes = InformeCapacitacion.objects.filter(
            idempleadocapacitacion__idcapacitacion=idcapacitacion,
            estado=True
        )

        serializer = self.get_serializer(
            informes,
            many=True
        )

        return Response(serializer.data)
    
class InformeCapacitacionDocumentoViewSet(viewsets.ModelViewSet):
    queryset = InformeCapacitacionDocumento.objects.all()
    serializer_class = InformeCapacitacionDocumentoSerializer