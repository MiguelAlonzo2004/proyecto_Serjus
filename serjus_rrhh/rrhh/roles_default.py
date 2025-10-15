from django.db import migrations

def crear_roles_por_defecto(apps, schema_editor):
    Rol = apps.get_model('rrhh', 'Rol')

    roles = [
        "Coordinadores",
        "Acompañantes",
        "Contadores",
        "Secretarias",
    ]

    for nombre in roles:
        Rol.objects.get_or_create(
            nombrerol=nombre,
            defaults={
                "descripcion": f"Rol {nombre} creado por defecto",
                "estado": True,
                "idusuario": 1,  # usuario por defecto (puedes cambiarlo)
            },
        )

def eliminar_roles_por_defecto(apps, schema_editor):
    Rol = apps.get_model('tu_app', 'Rol')
    nombres = [
        "Coordinadores",
        "Acompañantes",
        "Contadores",
        "Secretarias",
    ]
    Rol.objects.filter(nombrerol__in=nombres).delete()
