from django.db import migrations

def crear_variables_y_criterios(apps, schema_editor):
    Variable = apps.get_model('rrhh', 'Variable')
    Criterio = apps.get_model('rrhh', 'Criterio')
    Tipoevaluacion = apps.get_model('rrhh', 'Tipoevaluacion')

    # 👇 crea o busca tipo evaluación
    tipo_eval, _ = Tipoevaluacion.objects.get_or_create(
        nombretipo="Periodo de prueba acompañantes",
        defaults={
            "idusuario": 1,
            "estado": True
        }
    )

    data = [
        {
            "variable": "ADAPTACIÓN AL PUESTO",
            "criterios": [
                "Comprensión de funciones del puesto",
                "Cumplimiento de tareas asignadas",
                "Capacidad de aprendizaje",
                "Adaptación a normas y procedimientos",
                "Uso de herramientas de trabajo",
            ]
        },
        {
            "variable": "INTEGRACIÓN INSTITUCIONAL",
            "criterios": [
                "Identificación con los principios institucionales",
                "Comprensión general del planteamiento institucional",
                "Aplicación inicial del enfoque de género",
                "Comprensión general del trabajo territorial/sectorial",
                "Comprensión general de Educación Popular",
            ]
        },
        {
            "variable": "DESEMPEÑO INICIAL",
            "criterios": [
                "Calidad del trabajo",
                "Organización del trabajo",
                "Cumplimiento de tiempos",
                "Comunicación",
                "Redacción básica",
            ]
        },
        {
            "variable": "ACTITUD Y COMPETENCIAS",
            "criterios": [
                "Responsabilidad",
                "Puntualidad",
                "Trabajo en equipo",
                "Iniciativa",
                "Disposición para aprender",
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
            "INTEGRACIÓN INSTITUCIONAL",
            "DESEMPEÑO INICIAL",
            "ACTITUD Y COMPETENCIAS"
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0052_Nuevos_Tipos_Documento'),
    ]

    operations = [
        migrations.RunPython(crear_variables_y_criterios, eliminar_datos),
    ]