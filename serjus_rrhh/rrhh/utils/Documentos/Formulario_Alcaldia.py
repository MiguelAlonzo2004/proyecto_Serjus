from django.db import migrations
from rrhh.utils.formularios import crear_formulario_con_preguntas, eliminar_formulario


def crear_formulario_alcaldia_indigena(apps, schema_editor):

    preguntas = [
        {
            "texto": "¿Por qué el documento plantea que la Alcaldía Indígena no es un fin en sí misma sino un instrumento?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cómo influyó la colonización española en la transformación de las formas de autoridad indígena? Mencione al menos dos efectos concretos.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cuál es la relación entre legalidad y legitimidad en la constitución de la Alcaldía Indígena? ¿Por qué ambas son necesarias?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué papel juega el Convenio 169 y la Constitución en el reconocimiento de las Alcaldías Indígenas?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cuáles son los principales desafíos políticos que enfrentan actualmente las Alcaldías Indígenas?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué significa “refundar” la Alcaldía Indígena y por qué no se habla solo de “reconstituirla”? Argumenta con base en el texto.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cómo debe estructurarse la Alcaldía Indígena según el documento y por qué es importante integrar tanto autoridades tradicionales como organizaciones sectoriales (mujeres, jóvenes, guías espirituales, etc.)?",
            "tipo": "abierta"
        },

        {
            "texto": "¿Cuál es la base principal de la legitimidad de la Alcaldía Indígena?",
            "tipo": "opcion_multiple",
            "opciones": [
                "La aprobación del alcalde municipal",
                "La decisión de las asambleas comunitarias",
                "La inscripción legal en el registro civil",
                "El apoyo de organizaciones internacionales"
            ]
        },
        {
            "texto": "¿Cuál de las siguientes es una debilidad actual de las Alcaldías Indígenas?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Exceso de autonomía política",
                "Falta de reconocimiento comunitario",
                "Dependencia económica de las municipalidades",
                "Falta de estructura organizativa"
            ]
        },
        {
            "texto": "¿Cuál es uno de los objetivos principales de la refundación de la Alcaldía Indígena?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Sustituir al gobierno municipal",
                "Recuperar las tradiciones culturales",
                "Contribuir a la reconstrucción del Estado desde lo comunitario",
                "Crear una nueva estructura política independiente del Estado"
            ]
        },
    ]

    crear_formulario_con_preguntas(
        apps,
        titulo="La Refundación de la Alcaldía Indígena",
        descripcion="En base a la lectura del documento, responder las siguientes preguntas, si se tienen interrogantes sobre el mismo, consulte con el coordinador respectivo para poder ahondar en el análisis.",
        preguntas_data=preguntas
    )


def eliminar_formulario_alcaldia_indigena(apps, schema_editor):
    eliminar_formulario(apps, "La Refundación de la Alcaldía Indígena")