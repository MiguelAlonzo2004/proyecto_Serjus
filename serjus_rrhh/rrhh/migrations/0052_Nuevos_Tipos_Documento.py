# rrhh/migrations/XXXX_add_tipos_documento.py
from django.db import migrations

def crear_tipos_documento(apps, schema_editor):
    Tipodocumento = apps.get_model('rrhh', 'Tipodocumento')

    nuevos = [
        "Registro de Trastornos Musculoesqueléticos",
        "Registro enfermedades cronicas y degenerativas"
    ]

    for nombre in nuevos:
        Tipodocumento.objects.get_or_create(
            nombretipo=nombre,
            defaults={
                "descripcion": nombre,
                "estado": True,
                "idusuario": 1
            }
        )

class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0051_registroenfermedades_enfermedaddetalle'),
    ]

    operations = [
        migrations.RunPython(crear_tipos_documento),
    ]