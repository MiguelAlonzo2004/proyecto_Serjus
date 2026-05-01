from django.db import migrations
from rrhh.utils.formularios import crear_formulario_con_preguntas, eliminar_formulario


def crear_formulario_genero(apps, schema_editor):

    preguntas = [
        {
            "texto": "La Política de Equidad de Género de ASERJUS incorpora como elemento diferenciador:",
            "tipo": "opcion_multiple",
            "opciones": [
                "Enfoque de participación",
                "Feminismo como teoría y práctica política",
                "Los derechos legales",
                "Neutralidad de género"
            ]
        },
        {
            "texto": "El enfoque principal que utiliza ASERJUS para trabajar la equidad de género es:",
            "tipo": "opcion_multiple",
            "opciones": [
                "Mujeres en el Desarrollo (MED)",
                "Género en el Desarrollo (GED)",
                "Democracia en género",
                "Desarrollo sostenible"
            ]
        },
        {
            "texto": "La interseccionalidad permite:",
            "tipo": "opcion_multiple",
            "opciones": [
                "Analizar la desigualdad entre hombres y mujeres",
                "Comprender múltiples formas de desigualdad (género, etnia, clase, etc.)",
                "Aprender sobre factores culturales",
                "Aplicar soluciones iguales para todos"
            ]
        },
        {
            "texto": "Los feminismos decoloniales buscan:",
            "tipo": "opcion_multiple",
            "opciones": [
                "Reproducir modelos europeos que han sido funcionales",
                "Analizar opresiones en contextos latinoamericanos",
                "Centrarse en el análisis político",
                "Favorecer económicamente a las mujeres"
            ]
        },
        {
            "texto": "El enfoque de “territorio-cuerpo” implica:",
            "tipo": "opcion_multiple",
            "opciones": [
                "Separar lo personal de lo político",
                "Relacionar la defensa del territorio con el cuerpo de las personas",
                "Priorizar el cuidado ambiental",
                "Trabajar para erradicar la violencia de género"
            ]
        },

        {
            "texto": "¿Por qué la política de ASERJUS utiliza el concepto de equidad de género en lugar de igualdad de género? Explique con sus propias palabras.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Cómo se relaciona la equidad de género con la misión institucional de ASERJUS?",
            "tipo": "abierta"
        },
        {
            "texto": "Explique el enfoque de democracia en género y cómo transforma las relaciones entre hombres y mujeres.",
            "tipo": "abierta"
        },
        {
            "texto": "Describa el enfoque del feminismo comunitario y su importancia en contextos indígenas.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Por qué es importante incluir a los hombres en los procesos de equidad de género? Relaciónelo con el enfoque de nuevas masculinidades.",
            "tipo": "abierta"
        },
    ]

    crear_formulario_con_preguntas(
        apps,
        titulo="Política de Género Institucional",
        descripcion="En base a la lectura del documento, responder las siguientes preguntas, si se tienen interrogantes sobre el mismo, consulte con el coordinador respectivo para poder ahondar en el análisis.",
        preguntas_data=preguntas
    )


def eliminar_formulario_genero(apps, schema_editor):
    eliminar_formulario(apps, "Política de Género Institucional")