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
from .models import Formulario, Pregunta, Opcion, FormularioRespuesta, Respuesta, InduccionFormulario


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
        return url.replace("http://", "http://")  # 🔥 fuerza HTTPS

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
    formulario_respondido = serializers.SerializerMethodField()

    class Meta:
        model = Induccion
        fields = '__all__'

    def get_formulario_respondido(self, obj):
        request = self.context.get('request')
        user = request.user

        empleado = Empleado.objects.filter(usuario=user).first()

        if not empleado:
            print("❌ NO SE ENCONTRÓ EMPLEADO")
            return False

        formularios_ids = InduccionFormulario.objects.filter(
            idinduccion=obj,
            estado=True
        ).values_list('idformulario', flat=True)

        existe = FormularioRespuesta.objects.filter(
            idformulario__in=formularios_ids,
            idempleado=empleado,
            estado=True
        ).exists()

        return existe

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

#######################################################
#Induccion Formulario
class OpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = ['idopcion', 'texto', 'estado', 'orden']
        extra_kwargs = {
            'idpregunta': {'required': False}
        }

class PreguntaSerializer(serializers.ModelSerializer):
    opciones = OpcionSerializer(source='opcion_set', many=True, required=False)

    class Meta:
        model = Pregunta
        fields = ['idpregunta', 'texto', 'tipo', 'opciones']

class PreguntaCreateSerializer(serializers.ModelSerializer):
    opcion_set = OpcionSerializer(many=True, required=False)

    class Meta:
        model = Pregunta
        fields = ['texto', 'tipo', 'estado', 'idusuario', 'orden', 'opcion_set']
        extra_kwargs = {
            'texto': {'required': True},
            'tipo': {'required': True},
        }

class FormularioSerializer(serializers.ModelSerializer):
    preguntas = PreguntaSerializer(source='pregunta_set', many=True, read_only=True)

    class Meta:
        model = Formulario
        fields = '__all__'

    def get_preguntas(self, obj):
        preguntas = obj.pregunta_set.all().order_by('orden')
        return PreguntaSerializer(preguntas, many=True).data

class FormularioCreateSerializer(serializers.ModelSerializer):
    preguntas = PreguntaCreateSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Formulario
        fields = '__all__'

    def validate(self, data):
        idformulario = data.get('idformulario')
        idempleado = data.get('idempleado')

        existe = FormularioRespuesta.objects.filter(
            idformulario=idformulario,
            idempleado=idempleado
        ).exists()

        if existe:
            raise serializers.ValidationError(
                "Este formulario ya fue respondido por este empleado."
            )

        return data

    def update(self, instance, validated_data):
        print("VALIDATED DATA:", validated_data)
        preguntas_data = validated_data.pop('preguntas', None)

        # actualizar formulario
        instance.titulo = validated_data.get('titulo', instance.titulo)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.idusuario = validated_data.get('idusuario', instance.idusuario)
        instance.save()

        # 🔥 SOLO si vienen preguntas, se reemplazan
        if preguntas_data is not None:
            Opcion.objects.filter(idpregunta__idformulario=instance).delete()
            instance.pregunta_set.all().delete()

            for i, pregunta_data in enumerate(preguntas_data):
                opciones_data = pregunta_data.pop('opcion_set', [])

                pregunta = Pregunta.objects.create(
                    idformulario=instance,
                    orden=pregunta_data.get('orden', i + 1),
                    texto=pregunta_data['texto'],
                    tipo=pregunta_data['tipo'],
                    estado=pregunta_data.get('estado', True),
                    idusuario=pregunta_data['idusuario']
                )

                for j, opcion in enumerate(opciones_data):
                    Opcion.objects.create(
                        idpregunta=pregunta,
                        texto=opcion['texto'],
                        estado=opcion.get('estado', True),
                        orden=opcion.get('orden', j + 1)
                    )

        return instance

    def create(self, validated_data):
        print("VALIDATED DATA:", validated_data)
        preguntas_data = validated_data.pop('preguntas', [])
        formulario = Formulario.objects.create(**validated_data)

        for i, pregunta_data in enumerate(preguntas_data):
            opciones_data = pregunta_data.pop('opcion_set', [])

            # 🔥 DEBUG (te recomiendo dejarlo)
            print("PREGUNTA DATA:", pregunta_data)

            pregunta = Pregunta.objects.create(
                idformulario=formulario,
                orden=pregunta_data.get('orden', i + 1),
                texto=pregunta_data['texto'],
                tipo=pregunta_data['tipo'],
                estado=pregunta_data.get('estado', True),
                idusuario=pregunta_data['idusuario']  # 👈 ahora sí seguro viene
            )

            for j, opcion in enumerate(opciones_data):
                Opcion.objects.create(
                    idpregunta=pregunta,
                    texto=opcion['texto'],
                    estado=opcion.get('estado', True),
                    orden=opcion.get('orden', j + 1)
                )

        return formulario

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = '__all__'

    def get_opciones(self, obj):
        opciones = obj.opcion_set.all().order_by('orden')
        return OpcionSerializer(opciones, many=True).data

class FormularioRespuestaSerializer(serializers.ModelSerializer):
    respuestas = RespuestaSerializer(source='respuesta_set', many=True, read_only=True)

    class Meta:
        model = FormularioRespuesta
        fields = '__all__'

class RespuestaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = ['idpregunta', 'respuesta_texto', 'idopcion']

class FormularioRespuestaCreateSerializer(serializers.ModelSerializer):
    respuestas = RespuestaCreateSerializer(many=True, write_only=True)

    class Meta:
        model = FormularioRespuesta
        fields = '__all__'

    def create(self, validated_data):
        print("VALIDATED DATA:", validated_data)
        respuestas_data = validated_data.pop('respuestas', [])

        formulario_respuesta = FormularioRespuesta.objects.create(**validated_data)

        for respuesta_data in respuestas_data:
            Respuesta.objects.create(
                idformulariorespuesta=formulario_respuesta,
                **respuesta_data
            )

        return formulario_respuesta
    
class InduccionFormularioSerializer(serializers.ModelSerializer):
    class Meta:
        model = InduccionFormulario
        fields = '__all__'