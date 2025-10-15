from django.db import migrations

def crear_equipos_por_defecto(apps, schema_editor):
    Equipo = apps.get_model('rrhh', 'Equipo')

    equipos = [
        "Subregión Mam",
        "Subregión K'iché",
        "Subregión Metropolitana",
        "Subregión Ixcán",
        "Equipo Regionalización",
        "Equipo Sistema de Escuelas",
        "Equipo Defensa del Territorio",
        "Departamento Contable",
        "Secretaría y Conserjería",
        "Coordinaciones de Programa y Subprograma",
    ]

    for nombre in equipos:
        Equipo.objects.get_or_create(
            nombreequipo=nombre,
            defaults={
                "estado": True,
                "idusuario": 1,  # puedes ajustar el usuario por defecto
                "idcoordinador": None,
            },
        )

def eliminar_equipos_por_defecto(apps, schema_editor):
    Equipo = apps.get_model('tu_app', 'Equipo')
    nombres = [
        "Subregión Mam",
        "Subregión K'iché",
        "Subregión Metropolitana",
        "Subregión Ixcán",
        "Equipo Regionalización",
        "Equipo Sistema de Escuelas",
        "Equipo Defensa del Territorio",
        "Departamento Contable",
        "Secretaría y Conserjería",
        "Coordinaciones de Programa y Subprograma",
    ]
    Equipo.objects.filter(nombreequipo__in=nombres).delete()
