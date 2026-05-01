from django.db import migrations
from rrhh.utils.formularios import crear_formulario_con_preguntas, eliminar_formulario


def crear_formulario_capitalismo(apps, schema_editor):

    preguntas = [
        {
            "texto": "¿Cómo define el documento el concepto de “despojo” y por qué no se limita únicamente a la tierra? Explique al menos dos dimensiones del despojo.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué relación existe entre colonialismo histórico y las formas actuales de despojo?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Por qué el despojo es un proceso sistemático y no hechos aislados? Relaciónelo con estructuras de poder.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cómo ha impactado el despojo en la organización social de los pueblos indígenas? Explique las consecuencias sociales o culturales.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué papel ha jugado el Estado en los procesos de despojo?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Por qué se vincula el despojo con la pérdida de identidad cultural? Explique esta relación.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cómo se manifiestan actualmente las formas de despojo en los territorios? Dé ejemplos del tiempo actual.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Por qué el conocimiento de la historia es clave para enfrentar el despojo? Analice su importancia política.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué estrategias de resistencia o defensa menciona el documento frente al despojo? Explique al menos dos.",
            "tipo": "abierta"
        },

        {
            "texto": "Una comunidad pierde acceso a sus recursos naturales debido a proyectos externos aprobados por el Estado. Según el documento, ¿cómo se interpreta esta situación?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Como un proceso que genera desarrollo económico",
                "Como una mejora en la inversión pública",
                "Como una forma contemporánea de despojo vinculada a estructuras de poder",
                "Como un conflicto comunitario por los recursos"
            ]
        },
    ]

    crear_formulario_con_preguntas(
        apps,
        titulo="Capitalismo, Explotación e Injusticias",
        descripcion="En base a la lectura del documento, responder las siguientes preguntas, si se tienen interrogantes sobre el mismo, consulte con el coordinador respectivo para poder ahondar en el análisis.",
        preguntas_data=preguntas
    )


def eliminar_formulario_capitalismo(apps, schema_editor):
    eliminar_formulario(apps, "Capitalismo, Explotación e Injusticias")