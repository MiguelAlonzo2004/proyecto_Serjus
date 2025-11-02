# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import os
from django.conf import settings


class Amonestacion(models.Model): #YA
    idamonestacion = models.AutoField(db_column='idAmonestacion', primary_key=True)  # Field name made lowercase.
    idempleado = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='idEmpleado', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(max_length=20)
    fechaamonestacion = models.DateField(db_column='fechaAmonestacion')  # Field name made lowercase.
    motivo = models.CharField(max_length=150)
    iddocumento = models.TextField(db_column='idDocumento')  # Field name made lowercase.
    estado = models.BooleanField(default=True)  # This field type is a guess.
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'amonestacion'


class Aspirante(models.Model):
    idaspirante = models.AutoField(db_column='idAspirante', primary_key=True)
    nombreaspirante = models.CharField(db_column='nombreAspirante', max_length=100)
    apellidoaspirante = models.CharField(db_column='apellidoAspirante', max_length=100)
    nit = models.CharField(max_length=9)
    dpi = models.CharField(max_length=13, unique=True)
    genero = models.CharField(max_length=10)
    email = models.CharField(max_length=150)
    fechanacimiento = models.DateField(db_column='fechaNacimiento')
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=150)
    ididioma = models.ForeignKey(
        'Idioma', models.DO_NOTHING, db_column='idIdioma', blank=True, null=True
    )
    idpueblocultura = models.ForeignKey(
        'Pueblocultura', models.DO_NOTHING, db_column='idPuebloCultura', blank=True, null=True
    )
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField(db_column='idUsuario')
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = True
        db_table = 'aspirante'


class Ausencia(models.Model): #YA
    idausencia = models.AutoField(db_column='idAusencia', primary_key=True)  # Field name made lowercase.
    idempleado = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='idEmpleado', blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(max_length=50)
    diagnostico = models.TextField(blank=True, null=True)
    es_iggs = models.BooleanField(default=False, db_column='esIGSS') 
    otro = models.CharField(max_length=100, blank=True, null=True, db_column='otro')
    fechainicio = models.DateField(db_column='fechaInicio')  # Field name made lowercase.
    fechafin = models.DateField(db_column='fechaFin', blank=True, null=True)  # Field name made lowercase.
    cantidad_dias = models.IntegerField(blank=True, null=True, db_column='cantidadDias')
    iddocumento = models.IntegerField(db_column='idDocumento')  # Field name made lowercase.
    estado = models.BooleanField(default=True)  # This field type is a guess.
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'ausencia'


class Capacitacion(models.Model):
    idcapacitacion = models.AutoField(db_column='idCapacitacion', primary_key=True)  # Field name made lowercase.
    nombreevento = models.CharField(db_column='nombreEvento', max_length=150)  # Field name made lowercase.
    lugar = models.CharField(max_length=150)
    fechainicio = models.DateField(db_column='fechaInicio')  # Field name made lowercase.
    fechafin = models.DateField(db_column='fechaFin')  # Field name made lowercase.
    institucionfacilitadora = models.CharField(db_column='institucionFacilitadora', max_length=150)  # Field name made lowercase.
    montoejecutado = models.DecimalField(db_column='montoEjecutado', max_digits=10, decimal_places=2)  # Field name made lowercase.
    observacion = models.CharField(max_length=150, null=True, blank=True) 
    estado = models.BooleanField(default=True)  # This field type is a guess.
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'capacitacion'


class Contrato(models.Model): #YA
    idcontrato = models.AutoField(db_column='idContrato', primary_key=True)  # Field name made lowercase.
    idhistorialpuesto = models.ForeignKey('Historialpuesto', models.DO_NOTHING, db_column='idHistorialPuesto', blank=True, null=True)  # Field name made lowercase.
    fechainicio = models.DateField(db_column='fechaInicio')  # Field name made lowercase.
    fechafin = models.DateField(db_column='fechaFin', blank=True, null=True)  # Field name made lowercase.
    fechafirma = models.DateField(db_column='fechaFirma')  # Field name made lowercase.
    tipocontrato = models.CharField(db_column='tipoContrato', max_length=50)  # Field name made lowercase.
    estado = models.BooleanField(default=True)  # This field type is a guess.
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True) # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'contrato'


class Convocatoria(models.Model):
    idconvocatoria = models.AutoField(db_column='idConvocatoria', primary_key=True)  # Field name made lowercase.
    idpuesto = models.ForeignKey('Puesto', models.DO_NOTHING, db_column='idPuesto', blank=True, null=True)  # Field name made lowercase.
    nombreconvocatoria = models.CharField(db_column='nombreConvocatoria', max_length=500)  # Field name made lowercase.
    descripcion = models.CharField(max_length=5000)
    fechainicio = models.DateField(db_column='fechaInicio')  # Field name made lowercase.
    fechafin = models.DateField(db_column='fechaFin')  # Field name made lowercase.
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'convocatoria'


class Criterio(models.Model):
    idcriterio = models.AutoField(db_column='idCriterio', primary_key=True)
    idvariable = models.ForeignKey('Variable', models.DO_NOTHING, db_column='idVariable', blank=True, null=True)
    nombrecriterio = models.CharField(db_column='nombreCriterio', max_length=100)
    descripcioncriterio = models.CharField(db_column='descripcionCriterio', max_length=150)
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField(db_column='idUsuario')
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = True
        db_table = 'criterio'

def upload_document_path(instance, filename):
    # DOCUMENTOS DE ASPIRANTE
    if getattr(instance, 'idaspirante', None):
        folder_name = f"aspirante_{instance.idaspirante.idaspirante}/tipo_{instance.idtipodocumento.idtipodocumento}"
    
    # DOCUMENTOS DE EMPLEADO
    elif getattr(instance, 'idempleado', None):
        folder_name = f"empleado_{instance.idempleado.idempleado}/tipo_{instance.idtipodocumento.idtipodocumento}"
    
    else:
        # fallback si no hay relación (evita errores)
        folder_name = "otros"

    # Crear carpeta si no existe
    folder_path = os.path.join(settings.MEDIA_ROOT, 'documentos', folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Devolver la ruta final donde se almacenará el archivo
    return os.path.join('documentos', folder_name, filename)

class Documento(models.Model): #YA
    iddocumento = models.AutoField(primary_key=True)
    idtipodocumento = models.ForeignKey('Tipodocumento', models.DO_NOTHING, blank=True, null=True)
    idempleado = models.ForeignKey('Empleado', models.DO_NOTHING, blank=True, null=True)
    idaspirante = models.ForeignKey(Aspirante, models.DO_NOTHING, db_column='idAspirante', blank=True, null=True)
    archivo = models.FileField(upload_to=upload_document_path, max_length=255, null=True)  # <-- ahora es FileField
    nombrearchivo = models.CharField(max_length=150)
    mimearchivo = models.CharField(max_length=10)
    fechasubida = models.DateField()
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField()
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed=True
        db_table = 'documento'


class Empleado(models.Model): 
    idempleado = models.AutoField(db_column='idEmpleado', primary_key=True)
    idaspirante = models.ForeignKey(Aspirante, models.DO_NOTHING, db_column='idAspirante', blank=True, null=True)
    dpi = models.CharField(max_length=13, unique=True)
    nit = models.CharField(max_length=9)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    genero = models.CharField(max_length=10)
    lugarnacimiento = models.CharField(db_column='lugarNacimiento', max_length=100)
    fechanacimiento = models.DateField(db_column='fechaNacimiento')
    telefonocelular = models.CharField(db_column='telefonoCelular', max_length=10, blank=True, null=True)
    telefonoresidencial = models.CharField(db_column='telefonoResidencial', max_length=10, blank=True, null=True)
    telefonoemergencia = models.CharField(db_column='telefonoEmergencia', max_length=10, blank=True, null=True)
    titulonivelmedio = models.CharField(db_column='tituloNivelMedio', max_length=150, blank=True, null=True)
    estudiosuniversitarios = models.CharField(db_column='estudiosUniversitarios', max_length=150, blank=True, null=True)
    email = models.CharField(unique=True, max_length=150)
    direccion = models.CharField(max_length=150)
    estadocivil = models.CharField(db_column='estadoCivil', max_length=15)
    ididioma = models.ForeignKey('Idioma', models.DO_NOTHING, db_column='idIdioma', blank=True, null=True)
    idpueblocultura = models.ForeignKey('Pueblocultura', models.DO_NOTHING, db_column='idPuebloCultura', blank=True, null=True)
    numerohijos = models.IntegerField(db_column='numeroHijos')
    numeroiggs = models.CharField(db_column='numeroIggs', max_length=50, blank=True, null=True)
    idequipo = models.ForeignKey('Equipo', models.DO_NOTHING, db_column='idEquipo', blank=True, null=True)
    idpuesto = models.ForeignKey('Puesto', models.DO_NOTHING, db_column='idPuesto', blank=True, null=True)
    inicioLaboral = models.DateTimeField(db_column='inicioLaboral', auto_now_add=True, blank=True, null=True)
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField(db_column='idUsuario')
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    
    class Meta:
        managed=True
        db_table = 'Empleado'


class Empleadocapacitacion(models.Model):
    idempleadocapacitacion = models.AutoField(db_column='idEmpleadoCapacitacion', primary_key=True)  # Field name made lowercase.
    idempleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='idEmpleado', blank = True, null = True)  # Field name made lowercase.
    idcapacitacion = models.ForeignKey(Capacitacion, models.DO_NOTHING, db_column='idCapacitacion', blank=True, null=True)  # Field name made lowercase.
    asistencia = models.TextField(blank=True, null=True)  # This field type is a guess.
    fechaenvio = models.DateField(db_column='fechaEnvio', blank=True, null=True)   # Field name made lowercase.
    iddocumento = models.ForeignKey('Documento', models.DO_NOTHING, db_column='idDocumento', blank=True, null=True)  
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'empleadocapacitacion'


class Equipo(models.Model):
    idequipo = models.AutoField(db_column='idEquipo', primary_key=True)
    idcoordinador = models.IntegerField(db_column='idCoordinador', null=True)
    nombreequipo = models.CharField(db_column='nombreEquipo', max_length=100)
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField(db_column='idUsuario')
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = True
        db_table = 'equipo'

    def __str__(self):
        return self.nombreequipo


class Estado(models.Model): #YA
    idestado = models.AutoField(db_column='idEstado', primary_key=True)  # Field name made lowercase.
    nombreestado = models.CharField(db_column='nombreEstado', max_length=250)  # Field name made lowercase.
    descripcion = models.CharField(max_length=250)
    estado = models.BooleanField()  # This field type is a guess.
    idusuario = models.IntegerField(db_column='idUsuario', default=1)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'estado'


class Evaluacion(models.Model):
    idevaluacion = models.AutoField(db_column='idEvaluacion', primary_key=True)
    idempleado = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='idEmpleado', blank=True, null=True)
    modalidad = models.CharField(db_column='modalidad', max_length=20, blank=True, null=True)
    fechaevaluacion = models.DateTimeField(db_column='fechaEvaluacion')
    puntajetotal = models.DecimalField(db_column='puntajeTotal', max_digits=10, decimal_places=2)
    observacion = models.CharField(db_column='observacion', max_length=150)
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField(db_column='idUsuario')
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    idpostulacion = models.ForeignKey('Postulacion', models.DO_NOTHING, db_column='idPostulacion', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'evaluacion'


class Evaluacioncriterio(models.Model):
    idevaluacioncriterio = models.AutoField(db_column='idEvaluacionCriterio', primary_key=True)
    puntajecriterio = models.DecimalField(db_column='puntajeCriterio', max_digits=10, decimal_places=2)
    observacion = models.CharField(db_column='observacion', max_length=100, blank=True, null=True)
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField(db_column='idUsuario')
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    idevaluacion = models.ForeignKey('Evaluacion', models.DO_NOTHING, db_column='idEvaluacion', blank=True, null=True)
    idcriterio = models.ForeignKey('Criterio', models.DO_NOTHING, db_column='idCriterio', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'evaluacioncriterio'


class Historialpuesto(models.Model): #YA
    idhistorialpuesto = models.AutoField(db_column='idHistorialPuesto', primary_key=True)  # Field name made lowercase.
    idempleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='idEmpleado', blank = True, null = True)  # Field name made lowercase.
    idpuesto = models.ForeignKey('Puesto', models.DO_NOTHING, db_column='idPuesto', blank = True, null = True)  # Field name made lowercase.
    fechainicio = models.DateField(db_column='fechaInicio')  # Field name made lowercase.
    fechafin = models.DateField(db_column='fechaFin', blank=True, null=True)  # Field name made lowercase.
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    observacion = models.CharField(max_length=150)
    estado = models.BooleanField(default=True)  # This field type is a guess.
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'historialpuesto'


class Idioma(models.Model): #YA
    ididioma = models.AutoField(db_column='idIdioma', primary_key=True)  # Field name made lowercase.
    nombreidioma = models.CharField(db_column='nombreIdioma', max_length=20)  # Field name made lowercase.
    estado = models.BooleanField(default=True)  # This field type is a guess.
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'idioma'


class Induccion(models.Model):
    idinduccion = models.AutoField(db_column='idInduccion', primary_key=True)  # Field name made lowercase.
    fechainicio = models.DateField(db_column='fechaInicio')  # Field name made lowercase.
    fechafin = models.DateField(db_column='fechaFin')  # Field name made lowercase.
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'induccion'


class Inducciondocumento(models.Model):
    idinducciondocumento = models.AutoField(db_column='idInduccionDocumento', primary_key=True)  # Field name made lowercase.
    idinduccion = models.ForeignKey(Induccion, models.DO_NOTHING, db_column='idInduccion', blank=True, null=True)  # Field name made lowercase.
    iddocumento = models.ForeignKey(Documento, models.DO_NOTHING, db_column='idDocumento', blank=True, null=True)  # Field name made lowercase.
    fechaasignado = models.DateField(db_column='fechaAsignado')  # Field name made lowercase.
    fechacompletado = models.DateField(db_column='fechaCompletado', blank=True, null=True)  # Field name made lowercase.
    idinforme = models.IntegerField(db_column='idInforme')  # Field name made lowercase.
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True) # Field name made lowercase.
    idempleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='idEmpleado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'inducciondocumento'


class Postulacion(models.Model):
    idpostulacion = models.AutoField(db_column='idPostulacion', primary_key=True)  # Field name made lowercase.
    idaspirante = models.ForeignKey(Aspirante, models.DO_NOTHING, db_column='idAspirante', blank=True, null=True)  # Field name made lowercase.
    idconvocatoria = models.ForeignKey(Convocatoria, models.DO_NOTHING, db_column='idConvocatoria', blank=True, null=True)  # Field name made lowercase.
    fechapostulacion = models.DateField(db_column='fechaPostulacion')  # Field name made lowercase.
    idestado = models.ForeignKey(
        'Estado', models.DO_NOTHING, db_column='idEstado', blank=True, null=True
    ) 
    estado = models.BooleanField(default=True)
    observacion = models.CharField(max_length=150)
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'postulacion'
        unique_together = ('idaspirante', 'idconvocatoria')


class Pueblocultura(models.Model): #Ya
    idpueblocultura = models.AutoField(db_column='idPuebloCultura', primary_key=True)  # Field name made lowercase.
    nombrepueblo = models.CharField(db_column='nombrePueblo', max_length=20)  # Field name made lowercase.
    estado = models.BooleanField(default=True)  # This field type is a guess.
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'pueblocultura'


class Puesto(models.Model): #YA
    idpuesto = models.AutoField(db_column='idPuesto', primary_key=True)  # Field name made lowercase.
    nombrepuesto = models.CharField(db_column='nombrePuesto', max_length=100)  # Field name made lowercase.
    descripcion = models.CharField(max_length=150)
    salariobase = models.DecimalField(db_column='salarioBase', max_digits=10, decimal_places=2)  # Field name made lowercase.
    estado = models.BooleanField(default=True)  # This field type is a guess.
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'puesto'


class Rol(models.Model): #YA
    idrol = models.AutoField(db_column='idRol', primary_key=True)  # Field name made lowercase.
    nombrerol = models.CharField(db_column='nombreRol', max_length=100)  # Field name made lowercase.
    descripcion = models.CharField(max_length=150)
    estado = models.BooleanField(default=True)  # This field type is a guess.
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'rol'


class Seguimiento(models.Model):
    idseguimiento = models.AutoField(db_column='idSeguimiento', primary_key=True)
    idresponsable = models.IntegerField(db_column='idResponsable')
    fechaproximarev = models.DateTimeField(db_column='fechaProximaRev')
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField(db_column='idUsuario')
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    idevaluacion = models.ForeignKey('Evaluacion', models.DO_NOTHING, db_column='idEvaluacion', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'seguimiento'


class Seguimientovariable(models.Model):
    idseguimientovariable = models.AutoField(db_column='idSeguimientoVariable', primary_key=True)
    accionmejora = models.TextField(db_column='accionMejora')
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField(db_column='idUsuario')
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)
    idvariable = models.ForeignKey('Variable', models.DO_NOTHING, db_column='idVariable', blank=True, null=True)
    idseguimiento = models.ForeignKey('Seguimiento', models.DO_NOTHING, db_column='idSeguimiento', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'seguimientovariable'


class Terminacionlaboral(models.Model): #YA
    idterminacionlaboral = models.AutoField(db_column='idTerminacionLaboral', primary_key=True)  # Field name made lowercase.
    tipoterminacion = models.CharField(db_column='tipoTerminacion', max_length=20)  # Field name made lowercase.
    fechaterminacion = models.DateField(db_column='fechaTerminacion')  # Field name made lowercase.
    causa = models.CharField(max_length=150, blank=True, null=True)
    observacion = models.CharField(max_length=150)
    iddocumento = models.IntegerField(db_column='idDocumento')  # Field name made lowercase.
    estado = models.BooleanField(default=True)  # This field type is a guess.
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.
    idcontrato = models.ForeignKey(Contrato, models.DO_NOTHING, db_column='idContrato', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'terminacionlaboral'

 
class Tipodocumento(models.Model): #YA
    idtipodocumento = models.AutoField(db_column='idTipoDocumento', primary_key=True)  # Field name made lowercase.
    nombretipo = models.CharField(db_column='nombreTipo', max_length=150)  # Field name made lowercase.
    cantidadrepetir = models.IntegerField(db_column='cantidadRepetir', blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(max_length=150)
    estado = models.BooleanField(default=True)  # This field type is a guess.
    idusuario = models.IntegerField(db_column='idUsuario')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'tipodocumento'


class Tipoevaluacion(models.Model):
    idtipoevaluacion = models.AutoField(db_column='idTipoEvaluacion', primary_key=True)
    nombretipo = models.CharField(db_column='nombreTipo', max_length=50)
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField(db_column='idUsuario')
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = True
        db_table = 'tipoevaluacion'


class Usuario(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True)  # Field name made lowercase.
    nombreusuario = models.CharField(db_column='nombreUsuario', max_length=100)  # Field name made lowercase.
    contrasena = models.CharField(max_length=150)
    estado = models.BooleanField(default=True)  # This field type is a guess.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    idrol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='idRol', blank=True, null=True)  # Field name made lowercase.
    idempleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='idEmpleado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed=True
        db_table = 'usuario'


class Variable(models.Model):
    idvariable = models.AutoField(db_column='idVariable', primary_key=True)
    idtipoevaluacion = models.ForeignKey('Tipoevaluacion', models.DO_NOTHING, db_column='idTipoEvaluacion', blank=True, null=True)
    nombrevariable = models.CharField(db_column='nombreVariable', max_length=50)
    estado = models.BooleanField(default=True)
    idusuario = models.IntegerField(db_column='idUsuario')
    createdat = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updatedat = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = True
        db_table = 'variable'
