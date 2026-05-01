def crear_formulario_con_preguntas(apps, titulo, descripcion, preguntas_data):
    Formulario = apps.get_model('rrhh', 'Formulario')
    Pregunta = apps.get_model('rrhh', 'Pregunta')
    Opcion = apps.get_model('rrhh', 'Opcion')

    formulario, _ = Formulario.objects.get_or_create(
        titulo=titulo,
        defaults={
            "descripcion": descripcion,
            "estado": True,
            "idusuario": 1
        }
    )

    for i, p in enumerate(preguntas_data, start=1):
        pregunta = Pregunta.objects.create(
            idformulario=formulario,
            texto=p["texto"],
            tipo=p["tipo"],
            orden=i,
            estado=True,
            idusuario=1
        )

        if p["tipo"] == "opcion_multiple":
            for opcion in p["opciones"]:
                # Soporta string simple o dict (para futuro con respuestas correctas)
                if isinstance(opcion, dict):
                    texto_opcion = opcion["texto"]
                else:
                    texto_opcion = opcion

                Opcion.objects.create(
                    idpregunta=pregunta,
                    texto=texto_opcion,
                    estado=True
                )

def eliminar_formulario(apps, titulo):
    Formulario = apps.get_model('rrhh', 'Formulario')
    Formulario.objects.filter(titulo=titulo).delete()