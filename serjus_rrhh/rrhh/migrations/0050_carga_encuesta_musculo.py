from django.db import migrations


def crear_encuesta(apps, schema_editor):

    Formulario = apps.get_model('rrhh', 'Formulario')
    Pregunta = apps.get_model('rrhh', 'Pregunta')
    Opcion = apps.get_model('rrhh', 'Opcion')
    Dimension = apps.get_model('rrhh', 'Dimension')
    Induccion = apps.get_model('rrhh', 'Induccion')

    if Formulario.objects.filter(titulo="Encuesta Musculoesquelética").exists():
        return

    induccion = Induccion.objects.first()

    formulario = Formulario.objects.create(
        idinduccion=induccion,
        titulo="Encuesta Musculoesquelética",
        descripcion="Evaluación anual de trastornos musculoesqueléticos",
        idusuario=1,
        tipo = "medico"
    )

    zonas = [
        "CUELLO",
        "HOMBRO",
        "DORSAL / LUMBAR",
        "CODO / ANTEBRAZO",
        "MUÑECA / BRAZO",
        "RODILLA"
    ]

    dimensiones = []
    for z in zonas:
        dim, _ = Dimension.objects.get_or_create(nombre=z)
        dimensiones.append(dim)

    preguntas_base = [
        {
            "texto": "¿Ha tenido molestias en?",
            "tipo": "opcion_multiple",
            "opciones": ["Sí", "No"]
        },
        {
            "texto": "Si las ha tenido ¿Desde hace cuánto tiempo?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Ha tenido molestias en los últimos 6 meses?",
            "tipo": "opcion_multiple",
            "opciones": ["Sí", "No"]
        },
        {
            "texto": "Si tuvo molestias los últimos 6 meses ¿Cuánto tiempo duró dicha molestia?",
            "tipo": "opcion_multiple",
            "opciones": [
                "1 a 7 días",
                "8 a 30 días",
                "Más de 30 días",
                "Todos los días"
            ]
        },
        {
            "texto": "¿Necesitó atención médica para esta molestia?",
            "tipo": "opcion_multiple",
            "opciones": ["Sí", "No"]
        },
        {
            "texto": "¿Recibió tratamiento médico para esta molestia?",
            "tipo": "opcion_multiple",
            "opciones": ["Sí", "No"]
        }
    ]

    orden_global = 1

    for dim in dimensiones:
        for base in preguntas_base:

            pregunta = Pregunta.objects.create(
                idformulario=formulario,
                texto=base["texto"],
                tipo=base["tipo"],
                orden=orden_global,
                iddimension=dim,
                idusuario=1
            )

            if base["tipo"] == "opcion_multiple":
                for i, op in enumerate(base["opciones"], start=1):
                    Opcion.objects.create(
                        idpregunta=pregunta,
                        texto=op,
                        orden=i
                    )

            orden_global += 1

    # 🔹 Pregunta final
    pregunta_final = Pregunta.objects.create(
        idformulario=formulario,
        texto="¿Cuántas veces en este año, ha tenido dolor en la espalda específicamente?",
        tipo="opcion_multiple",
        orden=orden_global,
        idusuario=1
    )

    opciones_final = [
        "1 vez al año",
        "2 a 3 veces al año",
        "4 a 5 veces al año",
        "Más de 5 veces al año"
    ]

    for i, op in enumerate(opciones_final, start=1):
        Opcion.objects.create(
            idpregunta=pregunta_final,
            texto=op,
            orden=i
        )


def eliminar_encuesta(apps, schema_editor):
    Formulario = apps.get_model('rrhh', 'Formulario')
    Formulario.objects.filter(titulo="Encuesta Musculoesquelética").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0049_alter_formulariorespuesta_unique_together_and_more'), 
    ]

    operations = [
        migrations.RunPython(crear_encuesta, eliminar_encuesta),
    ]