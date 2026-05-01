from django.db import migrations
from rrhh.utils.formularios import crear_formulario_con_preguntas, eliminar_formulario


def crear_formulario_proyecto_politico(apps, schema_editor):

    preguntas = [
        {
            "texto": "¿Qué se entiende por “proyecto político aglutinador” y en qué se diferencia de una agenda de desarrollo o planificación territorial?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Por qué se plantea la necesidad de “aglutinar” diferentes actores sociales? Analice qué problemas busca resolver esta articulación.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Por qué se resalta la importancia de la articulación entre lo local y lo nacional? Analice cómo esto fortalece el proceso político.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué desafíos implica mantener la unidad entre actores con intereses distintos? Proponga al menos dos estrategias para enfrentarlos.",
            "tipo": "abierta"
        },
        {
            "texto": "Desde una perspectiva crítica: ¿cuáles son los principales obstáculos para construir un proyecto político aglutinador en la práctica y cómo podrían superarse? Proponga al menos dos soluciones.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cuáles son las reivindicaciones inmediatas coyunturales y las reivindicaciones a largo plazo que deben incluirse en la construcción de todo Proyecto Político Aglutinador?",
            "tipo": "abierta"
        },

        {
            "texto": "¿Cuál es la base fundamental para la construcción del proyecto político aglutinador?",
            "tipo": "opcion_multiple",
            "opciones": [
                "La democracia",
                "Los recursos económicos",
                "La organización participativa desde la comunidad",
                "Los despojos"
            ]
        },
        {
            "texto": "¿Qué es la Refundación del Estado según el documento?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cuáles son algunas herramientas que pueden servirnos para construir el proyecto político aglutinador?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Los planes de desarrollo, los grupos comunitarios y sus propias demandas",
                "Las asambleas comunitarias, las coordinadoras municipales y la formación política",
                "Los partidos políticos, los gobiernos municipales y las agendas sectoriales",
                "La articulación, la construcción colectiva y las decisiones conjuntas"
            ]
        },
        {
            "texto": "¿Con quiénes podemos trabajar para construir y avanzar en un proyecto político aglutinador?",
            "tipo": "abierta"
        },
    ]

    crear_formulario_con_preguntas(
        apps,
        titulo="Proyecto Político Aglutinador",
        descripcion="En base a la lectura del documento, responder las siguientes preguntas, si se tienen interrogantes sobre el mismo, consulte con el coordinador respectivo para poder ahondar en el análisis.",
        preguntas_data=preguntas
    )


def eliminar_formulario_proyecto_politico(apps, schema_editor):
    eliminar_formulario(apps, "Proyecto Político Aglutinador")