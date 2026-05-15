from django.db import migrations


def crear_variables_y_criterios(apps, schema_editor):
    Variable = apps.get_model('rrhh', 'Variable')
    Criterio = apps.get_model('rrhh', 'Criterio')
    Tipoevaluacion = apps.get_model('rrhh', 'Tipoevaluacion')

    # 👇 crea o busca tipo evaluación
    tipo_eval, _ = Tipoevaluacion.objects.get_or_create(
        nombretipo="Periodo de prueba coordinaciones",
        defaults={
            "idusuario": 1,
            "estado": True
        }
    )

    data = [
        {
            "variable": "ADAPTACIÓN AL PUESTO",
            "criterios": [
                "Comprensión del rol de coordinación",
                "Organización del equipo",
                "Adaptación a normativas",
                "Manejo de responsabilidades",
                "Priorización del trabajo",
            ]
        },
        {
            "variable": "COMUNICACIÓN Y LIDERAZGO",
            "criterios": [
                "Comunicación con el equipo",
                "Escucha activa",
                "Retroalimentación al equipo",
                "Manejo de conflictos y resolución de problemas",
                "Relación con otros equipos",
            ]
        },
        {
            "variable": "TOMA DE DECISIONES",
            "criterios": [
                "Toma de decisiones oportuna",
                "Delegación de tareas",
                "Seguimiento a acuerdos",
                "Información a coordinación superior sobre las decisiones y seguimiento",
            ]
        },
        {
            "variable": "ENFOQUE INSTITUCIONAL",
            "criterios": [
                "Comprensión general del planteamiento estratégico",
                "Aplicación metodológica de la educación popular",
                "Comprensión del enfoque de género",
                "Identificación institucional",
            ]
        },
        {
            "variable": "DESARROLLO DEL EQUIPO",
            "criterios": [
                "Acompañamiento al equipo",
                "Trabajo en equipo",
                "Motivación al equipo",
                "Desarrollo de capacidades",
            ]
        },
    ]

    for grupo in data:
        variable = Variable.objects.create(
            nombrevariable=grupo["variable"],
            idtipoevaluacion=tipo_eval,
            idusuario=1,
            estado=True,
        )

        for criterio in grupo["criterios"]:
            Criterio.objects.create(
                idvariable=variable,
                nombrecriterio=criterio,
                descripcioncriterio=criterio,
                idusuario=1,
                estado=True
            )


def eliminar_datos(apps, schema_editor):
    Variable = apps.get_model('rrhh', 'Variable')

    Variable.objects.filter(
        nombrevariable__in=[
            "ADAPTACIÓN AL PUESTO",
            "COMUNICACIÓN Y LIDERAZGO",
            "TOMA DE DECISIONES",
            "ENFOQUE INSTITUCIONAL",
            "DESARROLLO DEL EQUIPO"
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0055_alter_evaluacion_observacion_and_more'),
    ]

    operations = [
        migrations.RunPython(
            crear_variables_y_criterios,
            eliminar_datos
        ),
    ]