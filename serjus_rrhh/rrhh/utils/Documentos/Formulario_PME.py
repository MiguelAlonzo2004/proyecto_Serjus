from django.db import migrations
from rrhh.utils.formularios import crear_formulario_con_preguntas, eliminar_formulario


def crear_formulario_induccion(apps, schema_editor):

    preguntas = [
        {
            "texto": "¿Cuál es la diferencia entre planificar “para” la comunidad y planificar “con” la comunidad? Analice cómo cambia el resultado del proceso.",
            "tipo": "abierta"
        },
        {
            "texto": "El documento propone varias fases dentro del proceso de planificación. ¿Por qué es importante seguir estas fases y no improvisar acciones? Relaciónelo con la sostenibilidad de los proyectos.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué relación existe entre los objetivos estratégicos y los proyectos? Explique por qué no deben formularse de manera aislada.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Por qué es importante definir indicadores dentro del PME? Explique cómo ayudan en el seguimiento y evaluación.",
            "tipo": "abierta"
        },
        {
            "texto": "El documento menciona la importancia del seguimiento y evaluación. ¿Qué consecuencias tendría no realizar el seguimiento y evaluación de una planificación?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué papel juegan los actores locales (comunidad, autoridades, organizaciones) en la implementación del PME?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cómo puede el PME contribuir a mejorar la transparencia y la rendición de cuentas en la gestión municipal? Relaciónelo con la participación ciudadana.",
            "tipo": "abierta"
        },

        {
            "texto": "Una municipalidad inicia proyectos sin realizar diagnóstico previo. Según el enfoque del PME, ¿qué problema es más probable que ocurra?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Mayor rapidez en la ejecución",
                "Uso eficiente de los recursos",
                "Desalineación entre proyectos y necesidades reales",
                "Mayor participación ciudadana"
            ]
        },
        {
            "texto": "Si en un proceso de planificación solo participan técnicos municipales y no la comunidad, ¿qué implicación tiene según el documento?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Mejora la calidad técnica del plan",
                "Se garantiza una implementación más rápida",
                "Se debilita la legitimidad y pertinencia del plan",
                "Se reduce la complejidad del proceso"
            ]
        },
        {
            "texto": "Si un plan no se ajusta cuando cambian las condiciones del contexto (por ejemplo, crisis o nuevos problemas), ¿qué falla del PME se evidencia?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Falta de diagnóstico",
                "Falta de participación",
                "Falta de flexibilidad en la planificación",
                "Falta de recursos económicos"
            ]
        },
    ]

    crear_formulario_con_preguntas(
        apps,
        titulo="Documento Sistema PME",
        descripcion="En base a la lectura del documento, responder las siguientes preguntas, si se tienen interrogantes sobre el mismo, consulte con el coordinador respectivo para poder ahondar en el análisis.",
        preguntas_data=preguntas
    )


def eliminar_formulario_induccion(apps, schema_editor):
    eliminar_formulario(apps, "Documento Sistema PME")