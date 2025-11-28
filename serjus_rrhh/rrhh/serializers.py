from rest_framework import serializers
from .models import Empleado, Amonestacion, Aspirante
from django.contrib.auth.hashers import make_password
from .models import Capacitacion, Empleadocapacitacion, Evaluacion, Evaluacioncriterio, Criterio, Postulacion
from .models import (
    Ausencia, Contrato, Convocatoria, Documento, 
    Equipo, Historialpuesto, Idioma, 
    Induccion, Inducciondocumento, Puesto, Rol, Terminacionlaboral, Tipodocumento, Usuario, 
    Estado, Pueblocultura, Postulacion, Variable, Tipoevaluacion, Seguimiento, Seguimientovariable
)
class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__' 

class PostulacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postulacion
        fields = '__all__'

class PuebloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pueblocultura
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'

class AmonestacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amonestacion
        fields = '__all__'

class AspiranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aspirante
        fields = '__all__' 

class CapacitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capacitacion
        fields = '__all__'

class EmpleadocapacitacionSerializer(serializers.ModelSerializer):
    idempleado = serializers.PrimaryKeyRelatedField(queryset=Empleado.objects.all())
    idcapacitacion = serializers.PrimaryKeyRelatedField(queryset=Capacitacion.objects.all())
    
    class Meta:
        model = Empleadocapacitacion
        fields = '__all__'


class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = '__all__'

class CriterioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criterio
        fields = '__all__'

class EvaluacioncriterioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacioncriterio
        fields = '__all__'
        
class AusenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ausencia
        fields = '__all__'

class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = '__all__'

class ConvocatoriaSerializer(serializers.ModelSerializer):
    nombrepuesto = serializers.CharField(source='idpuesto.nombrepuesto', read_only=True)
    fechainicio = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    fechafin = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"], allow_null=True)

    # 👇 Aquí viene el truco: mostrar el estado como objeto
    idestado = EstadoSerializer(read_only=True)

    # 👇 Y aceptar el ID numérico al crear o editar
    idestado_id = serializers.PrimaryKeyRelatedField(
        queryset=Estado.objects.all(),
        source='idestado',
        write_only=True
    )

    class Meta:
        model = Convocatoria
        fields = '__all__'

class DocumentoSerializer(serializers.ModelSerializer):
    archivo = serializers.FileField(required=False, allow_null=True)
    archivo_url = serializers.SerializerMethodField()

    class Meta:
        model = Documento
        fields = '__all__'

    def get_archivo_url(self, obj):
        if not obj.archivo:
            return None

        request = self.context.get('request')
        url = request.build_absolute_uri(obj.archivo.url) if request else obj.archivo.url
        return url.replace("http://", "https://")  # 🔥 fuerza HTTPS

    def update(self, instance, validated_data):
        request = self.context.get('request')

        # Si se indicó que se borre el archivo
        if request and request.data.get('borrar_archivo') == 'true':
            if instance.archivo:
                instance.archivo.delete(save=False)
            instance.archivo = None
            instance.mimearchivo = "-----"
            instance.nombrearchivo = f"{instance.nombrearchivo} (archivo eliminado)"

        # Si se sube nuevo archivo
        if 'archivo' in validated_data:
            instance.archivo = validated_data.get('archivo')

        # Mantener mimearchivo siempre presente
        if not validated_data.get('mimearchivo'):
            validated_data['mimearchivo'] = '-----'

        return super().update(instance, validated_data)


class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'

class HistorialpuestoSerializer(serializers.ModelSerializer):
    nombre_puesto = serializers.CharField(source='idpuesto.nombrepuesto', read_only=True)

    class Meta:
        model = Historialpuesto
        fields = '__all__'
        # El campo nombre_puesto estará disponible en la respuesta

class IdiomaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idioma
        fields = '__all__'

class InduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Induccion
        fields = '__all__'

class InducciondocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inducciondocumento
        fields = '__all__'

class PuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puesto
        fields = '__all__'  

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class TerminacionlaboralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminacionlaboral
        fields = '__all__'  

class TipodocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipodocumento
        fields = '__all__'  

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {
            'contrasena': {'required': False}, 
        }

    def create(self, validated_data):
        if 'contrasena' in validated_data:
            validated_data['contrasena'] = make_password(validated_data['contrasena'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        contrasena = validated_data.pop('contrasena', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if contrasena:
            instance.contrasena = make_password(contrasena)

        instance.save()
        return instance 

class SeguimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguimiento
        fields = '__all__'

class SeguimientoVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguimientovariable
        fields = '__all__'

class TipoevaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipoevaluacion
        fields = '__all__'

class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = '__all__'