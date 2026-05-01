from django.db import migrations
from rrhh.utils.formularios import crear_formulario_con_preguntas, eliminar_formulario


def crear_formulario_plan_multianual(apps, schema_editor):

    preguntas = [
        {
            "texto": "¿Cuál fue uno de los principales motivos para la creación de SERJUS?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Implementar proyectos productivos",
                "Apoyar la recuperación de comunidades afectadas por el conflicto armado",
                "Desarrollar organizaciones rurales",
                "Promover la educación formal"
            ]
        },
        {
            "texto": "Explique por qué la organización comunitaria es considerada el eje central del trabajo de SERJUS.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cómo se relaciona la cosmovisión maya con el planteamiento de desarrollo que propone SERJUS?",
            "tipo": "abierta"
        },
        {
            "texto": "Explique la importancia de la participación de las mujeres dentro del planteamiento institucional.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Por qué la defensa del territorio es un elemento clave en el trabajo de SERJUS?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cuál es el papel de la educación popular en la transformación social que propone SERJUS?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué significa construir un Estado plurinacional y por qué es importante para los pueblos indígenas?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cómo se vinculan los principios institucionales (como solidaridad, reciprocidad y colectividad) con las acciones concretas de SERJUS?",
            "tipo": "abierta"
        },
        {
            "texto": "Explique la importancia de la articulación entre lo local, municipal, regional y nacional.",
            "tipo": "abierta"
        },

        {
            "texto": "¿Cuáles son los principales retos estructurales identificados en el Plan Multianual?",
            "tipo": "opcion_multiple",
            "opciones": [
                "El sistema jurídico, los despojos, la economía nacional, la desigualdad.",
                "Concentración de la tierra y recursos, el sistema jurídico político, la exclusión de la población indígena y de las mujeres.",
                "Bajo acceso a recursos, el colonialismo, la agro exportación",
                "Escasa inversión extranjera, concentración de la tierra, el extractivismo."
            ]
        },

        {
            "texto": "Explique con sus propias palabras la Misión y Visión de SERJUS.",
            "tipo": "abierta"
        },
        {
            "texto": "Explique la relación que debe darse entre las estrategias institucionales para el alcance de los objetivos y planteamiento institucional.",
            "tipo": "abierta"
        },
    ]

    crear_formulario_con_preguntas(
        apps,
        titulo="Plan Multianual",
        descripcion="En base a la lectura del documento, responder las siguientes preguntas, si se tienen interrogantes sobre el mismo, consulte con el coordinador respectivo para poder ahondar en el análisis.",
        preguntas_data=preguntas
    )


def eliminar_formulario_plan_multianual(apps, schema_editor):
    eliminar_formulario(apps, "Plan Multianual")