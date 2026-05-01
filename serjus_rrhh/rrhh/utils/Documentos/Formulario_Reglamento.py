from django.db import migrations
from rrhh.utils.formularios import crear_formulario_con_preguntas, eliminar_formulario


def crear_formulario_reglamento(apps, schema_editor):

    preguntas = [
        {
            "texto": "¿Cuál es el objetivo principal del Reglamento Interior de Trabajo?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Establecer salarios",
                "Regular las condiciones de trabajo",
                "Evaluar el desempeño",
                "Contratar personal"
            ]
        },
        {
            "texto": "¿Quién debe cumplir obligatoriamente el reglamento?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Solo la Junta Directiva",
                "Solo los trabajadores",
                "Trabajadores y empleador",
                "Solo el área administrativa"
            ]
        },
        {
            "texto": "¿Quién debe autorizar que un trabajador/a salga antes de su jornada o se ausente de sus labores?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Departamento contable",
                "Cualquier persona del equipo",
                "Jefe inmediato",
                "Nadie, tengo derecho a salir antes"
            ]
        },
        {
            "texto": "¿Cómo debe justificarse una ausencia por enfermedad?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Solo aviso verbal",
                "Con constancia o reporte médico o del IGSS",
                "Con mensaje de texto",
                "No es necesario ya saben que estoy enfermo/a"
            ]
        },

        {
            "texto": "Explique con sus propias palabras cuál es la importancia del reglamento para la organización y para los trabajadores de SERJUS.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué derechos laborales importantes para el trabajador/a reconoce el reglamento (mencione al menos tres)?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué obligaciones establecidas en el reglamento considera las más importantes para el trabajador/a y por qué?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cómo contribuye el cumplimiento del reglamento al buen funcionamiento de la organización?",
            "tipo": "abierta"
        },
        {
            "texto": "Explique la diferencia entre una falta leve y una falta grave dentro del contexto laboral y qué implicaciones tiene cada una de ellas para el trabajador.",
            "tipo": "abierta"
        },
        {
            "texto": "¿En qué situaciones un trabajador tiene derecho a recibir indemnización según el reglamento y la ley laboral?",
            "tipo": "abierta"
        },
    ]

    crear_formulario_con_preguntas(
        apps,
        titulo="Reglamento Interior de Trabajo",
        descripcion="En base a la lectura del documento, responder las siguientes preguntas, si se tienen interrogantes sobre el mismo, consulte con el coordinador respectivo para poder ahondar en el análisis.",
        preguntas_data=preguntas
    )


def eliminar_formulario_reglamento(apps, schema_editor):
    eliminar_formulario(apps, "Reglamento Interior de Trabajo")