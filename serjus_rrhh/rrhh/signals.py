from django.db.models.signals import post_migrate
from django.dispatch import receiver
from datetime import datetime, date
from django.contrib.auth.hashers import make_password
from .models import Usuario, Rol, Empleado, Tipodocumento, Tipoevaluacion, Estado  # <-- agregamos Estado

@receiver(post_migrate)
def create_default_admin_and_data(sender, **kwargs):
    """
    Crea datos por defecto después de aplicar migraciones en la app rrhh.
    Incluye usuario admin, tipos de documentos, tipos de evaluación y estados base.
    """
    if sender.name == "rrhh":  

        # === Crear rol Administrador ===
        rol_admin, _ = Rol.objects.get_or_create(
            nombrerol="Administrador",
            defaults={
                'descripcion': 'Rol con todos los permisos',
                'estado': True,
                'idusuario': 1,
            }
        )

        # === Crear empleado por defecto ===
        empleado_default, _ = Empleado.objects.get_or_create(
            dpi="0000000000000",
            defaults={
                'nit': "0000000",
                'nombre': "Empleado",
                'apellido': "Default",
                'genero': "Otro",
                'lugarnacimiento': "Ciudad Default",
                'fechanacimiento': date(1990, 1, 1),
                'telefonocelular': "0000000000",
                'telefonoresidencial': None,
                'telefonoemergencia': None,
                'email': "admin@example.com",
                'direccion': "Dirección Default",
                'estadocivil': "Soltero",
                'numerohijos': 0,
                'idusuario': 1,
                'estado': True
            }
        )

        # === Crear usuario admin ===
        if not Usuario.objects.filter(nombreusuario="admin").exists():
            Usuario.objects.create(
                nombreusuario="admin",
                contrasena=make_password("admin123"),
                estado=True,
                createdat=datetime.now(),
                updatedat=datetime.now(),
                idrol=rol_admin,
                idempleado=empleado_default
            )
            print("Usuario admin creado correctamente.")

        # === Tipos de documentos por defecto ===
        documentos_por_defecto = [
            "CURRICULUM ACREDITADO",
            "INFORME",
            "COMPROBANTE DE AUSENCIA",
            "LLAMADAS DE ATENCIÓN",
            "DOCUMENTOS DE INDUCCIÓN",
            "CONTRATO",
            "RECONOCIMIENTO",
        ]

        for nombre in documentos_por_defecto:
            Tipodocumento.objects.get_or_create(
                nombretipo=nombre,
                defaults={
                    'descripcion': nombre,
                    'estado': True,
                    'idusuario': 1
                }
            )
        print("Tipos de documentos por defecto creados correctamente.")

        # === Tipos de evaluación por defecto ===
        tipos_evaluacion = [
            "Coordinador",
            "Acompañante",
            "Administrativo",
            "Entrevista"
        ]

        for tipo in tipos_evaluacion:
            Tipoevaluacion.objects.get_or_create(
                nombretipo=tipo,
                defaults={
                    'estado': True,
                    'idusuario': 1
                }
            )
        print("Tipos de evaluación por defecto creados correctamente.")

        # === Estados por defecto (migrado desde la migración anterior) ===
        estados_aspirantes = [
            {"nombreestado": "Postulado", "descripcion": "Aspirante ha postulado"},
            {"nombreestado": "Seleccionado para Entrevista", "descripcion": "Aspirante seleccionado para entrevista"},
            {"nombreestado": "Rechazado", "descripcion": "Aspirante no continúa en el proceso"},
        ]

        estados_convocatorias = [
            {"nombreestado": "Abierta", "descripcion": "Convocatoria disponible para postulaciones activas."},
            {"nombreestado": "Cerrada", "descripcion": "Convocatoria cerrada. No se aceptan nuevas postulaciones."},
            {"nombreestado": "Finalizada", "descripcion": "Convocatoria finalizada. Se completó el proceso de selección."},
        ]

        todos_los_estados = estados_aspirantes + estados_convocatorias

        for e in todos_los_estados:
            Estado.objects.get_or_create(
                nombreestado=e["nombreestado"],
                defaults={
                    'descripcion': e["descripcion"],
                    'estado': True,
                    'idusuario': 1
                }
            )
        print("Estados por defecto creados correctamente.")
