from django.db import migrations
from rrhh.utils.formularios import crear_formulario_con_preguntas, eliminar_formulario


def crear_formulario_cocodes_maya(apps, schema_editor):

    preguntas = [
        {
            "texto": "¿Cómo se entiende el concepto de “reconstitución de los pueblos” y por qué va más allá de lo organizativo? Explique su dimensión histórica y cultural.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué significa la “refundación del Estado” desde la perspectiva de los pueblos indígenas? Analice en qué se diferencia del modelo actual de Estado.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cómo se articulan los COCODE con el sistema comunitario Maya según el documento? Explique si son compatibles o si existen tensiones.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué diferencias existen entre la lógica del sistema comunitario Maya y la lógica institucional del Estado? Mencione al menos dos diferencias clave.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Por qué la organización comunitaria no debe depender únicamente de estructuras legales del Estado? Analice los riesgos de esta dependencia.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cómo contribuyen los COCODE al fortalecimiento del poder comunitario cuando se articulan correctamente con el sistema Maya?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué riesgos existen cuando los COCODE se desvirtúan de su función original dentro de las comunidades? Explique las consecuencias.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué desafíos enfrenta la articulación entre estructuras comunitarias ancestrales y mecanismos modernos de participación como los COCODE?",
            "tipo": "abierta"
        },
        {
            "texto": "Desde una perspectiva crítica: ¿cómo pueden los COCODE fortalecer el sistema comunitario Maya sin perder su esencia frente a la institucionalidad estatal? Proponga al menos dos estrategias.",
            "tipo": "abierta"
        },

        {
            "texto": "Una comunidad decide seguir únicamente las normas del Estado y deja de lado sus formas propias de organización ancestral, ¿qué implicación tiene esto?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Fortalecimiento de la institucionalidad estatal",
                "Mejora en la eficiencia administrativa",
                "Debilitamiento de la identidad y el sistema comunitario propio",
                "Aumento en la participación ciudadana"
            ]
        },
        {
            "texto": "Una comunidad logra integrar el COCODE con sus autoridades ancestrales para tomar decisiones colectivas. ¿Qué concepto del documento se está aplicando?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Centralización del poder",
                "Sustitución del sistema comunitario",
                "Articulación entre sistema estatal y comunitario",
                "Dependencia institucional"
            ]
        },
    ]

    crear_formulario_con_preguntas(
        apps,
        titulo="COCODES en el Sistema Comunitario Maya",
        descripcion="En base a la lectura del documento, responder las siguientes preguntas, si se tienen interrogantes sobre el mismo, consulte con el coordinador respectivo para poder ahondar en el análisis.",
        preguntas_data=preguntas
    )


def eliminar_formulario_cocodes_maya(apps, schema_editor):
    eliminar_formulario(apps, "COCODES en el Sistema Comunitario Maya")