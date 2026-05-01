from django.db import migrations
from rrhh.utils.formularios import crear_formulario_con_preguntas, eliminar_formulario


def crear_formulario_haciendo_realidad(apps, schema_editor):

    preguntas = [
        {
            "texto": "El documento plantea el concepto de “buen vivir”. ¿En qué se diferencia del modelo tradicional de desarrollo económico? Explique al menos dos diferencias clave y sus implicaciones para las comunidades.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Por qué la “unidad en la diversidad” es un reto importante en la organización social?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Por qué es importante que las comunidades desarrollen capacidad de propuesta, gestión y presión? Relaciónelo con la incidencia política.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué significa construir un “poder alternativo” desde lo local y cuál es su finalidad? Explique con un ejemplo concreto.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cómo contribuye la organización comunitaria a la defensa del territorio frente a amenazas externas? Mencione al menos dos ejemplos.",
            "tipo": "abierta"
        },
        {
            "texto": "Desde una perspectiva crítica: ¿cuáles son los principales obstáculos y desafíos para lograr una organización participativa efectiva y cómo podrían superarse? Indique al menos 2 obstáculos y dos desafíos y proponga al menos dos soluciones.",
            "tipo": "abierta"
        },
        {
            "texto": "Una organización comunitaria solo trabaja proyectos para beneficiar a sus miembros directos, sin involucrar a toda la comunidad. Esto significa que:",
            "tipo": "opcion_multiple",
            "opciones": [
                "Es una organización comunitaria sectorial",
                "Está cumpliendo con el modelo de participación al realizar proyectos",
                "Tiene potencial, pero no es una verdadera organización participativa comunal",
                "Es el modelo ideal de organización para ejecutar proyectos grupales"
            ]
        },
        {
            "texto": "Si las comunidades fortalecen su organización y logran incidir en decisiones del gobierno municipal, ¿qué concepto del documento se está aplicando?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Centralización del poder",
                "Dependencia institucional",
                "Construcción de poder local alternativo",
                "Administración pública tradicional"
            ]
        },
        {
            "texto": "¿Cuáles de estos son los principios de la organización participativa de la comunidad?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Horizontalidad, articulación hacia lo macro, identidad cultural, protagonismo de las mujeres.",
                "Cosmovisión, Gobierno Ancestral, organización territorial y sectorial.",
                "Horizontalidad, generación de recursos, el buen vivir, la democracia.",
                "Construcción del poder local, fortalecimiento de la economía local, la formación política."
            ]
        },
        {
            "texto": "¿Qué se entiende por comunidad y cómo se articula la organización en el nivel comunitario?",
            "tipo": "abierta"
        },
        {
            "texto": "¿En qué consiste la propuesta de articulación municipal, cómo y con quienes se puede integrar?",
            "tipo": "abierta"
        },
        {
            "texto": "Explique cuál es la propuesta de articulación de las comunidades al espacio departamental, regional y nacional.",
            "tipo": "abierta"
        },
    ]

    crear_formulario_con_preguntas(
        apps,
        titulo="Haciendo Realidad el Sueño",
        descripcion="En base a la lectura del documento, responder las siguientes preguntas, si se tienen interrogantes sobre el mismo, consulte con el coordinador respectivo para poder ahondar en el análisis.",
        preguntas_data=preguntas
    )


def eliminar_formulario_haciendo_realidad(apps, schema_editor):
    eliminar_formulario(apps, "Haciendo Realidad el Sueño")