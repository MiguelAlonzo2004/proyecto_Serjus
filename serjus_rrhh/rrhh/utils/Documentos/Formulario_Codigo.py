from django.db import migrations
from rrhh.utils.formularios import crear_formulario_con_preguntas, eliminar_formulario


def crear_formulario_codigo_conducta(apps, schema_editor):

    preguntas = [
        {
            "texto": "¿Cuál es el propósito principal del Código?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Sancionar al personal que comete faltas",
                "Establecer normas y mecanismos que guíen la conducta y prácticas éticas",
                "Regular temas legales",
                "Controlar el desempeño del personal"
            ]
        },
        {
            "texto": "La salvaguarda se entiende como:",
            "tipo": "opcion_multiple",
            "opciones": [
                "Protección únicamente física",
                "Actitud de proteger integralmente a personas en riesgo",
                "Cumplimiento de normas legales",
                "Supervisión administrativa"
            ]
        },
        {
            "texto": "¿Quiénes deben cumplir el Código?",
            "tipo": "opcion_multiple",
            "opciones": [
                "El personal contratado",
                "Solo la Junta Directiva",
                "Toda persona vinculada a ASERJUS interna y externamente",
                "Voluntarios y practicantes"
            ]
        },
        {
            "texto": "El enfoque de protección o salvaguarda del código prioriza principalmente:",
            "tipo": "opcion_multiple",
            "opciones": [
                "A proveedores",
                "A personal administrativo",
                "A niñez, mujeres y adultos mayores",
                "A donantes que visitan los procesos acompañados"
            ]
        },
        {
            "texto": "¿Qué debe hacerse antes de tomar fotografías a los sujetos de acompañamiento o elaborar material audiovisual que los incluya y que será publicado?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Informar verbalmente al representante del grupo",
                "Pedir autorización escrita",
                "No es necesario pedir permiso, las personas saben al respecto.",
                "Avisarles después para que vean sus fotos"
            ]
        },
        {
            "texto": "¿Cuál es una práctica discriminatoria según el Código?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Promover participación",
                "Excluir por etnia o género",
                "Fomentar diálogo",
                "Respetar opiniones"
            ]
        },
        {
            "texto": "El principio de “tolerancia cero” aplica a:",
            "tipo": "opcion_multiple",
            "opciones": [
                "Errores administrativos",
                "Conductas indebidas como abuso, acoso, fraude, corrupción, discriminación.",
                "Retrasos laborales",
                "Diferencias de opinión entre personal"
            ]
        },
        {
            "texto": "¿Qué ocurre si una persona comete faltas referidas en este código?",
            "tipo": "opcion_multiple",
            "opciones": [
                "No pasa nada",
                "Se analiza la falta cometida y se vincula con las sanciones establecidas en el reglamento interior de trabajo",
                "Se incluye en el expediente del personal",
                "Se ignora, este código solo es un requisito"
            ]
        },

        {
            "texto": "¿Por qué es importante que el Código sea obligatorio para todo el personal y colaboradores, y no opcional?",
            "tipo": "abierta"
        },
        {
            "texto": "Indique cuáles son los actos y conductas no debidas o indeseables que establece el código de conducta.",
            "tipo": "abierta"
        },
        {
            "texto": "¿Qué riesgos institucionales se buscan evitar con las normas sobre fraude y corrupción?",
            "tipo": "abierta"
        },
        {
            "texto": "¿Por qué el Código establece que debe darse un comportamiento ético incluso fuera del horario laboral?",
            "tipo": "abierta"
        },
    ]

    crear_formulario_con_preguntas(
        apps,
        titulo="Código de Conducta",
        descripcion="En base a la lectura del documento, responder las siguientes preguntas, si se tienen interrogantes sobre el mismo, consulte con el coordinador respectivo para poder ahondar en el análisis.",
        preguntas_data=preguntas
    )


def eliminar_formulario_codigo_conducta(apps, schema_editor):
    eliminar_formulario(apps, "Código de Conducta")