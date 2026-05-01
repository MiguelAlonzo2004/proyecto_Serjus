from django.db import migrations
from rrhh.utils.formularios import crear_formulario_con_preguntas, eliminar_formulario


def crear_formulario_induccion(apps, schema_editor):

    preguntas = [
        {"texto": "¿Por qué se considera al municipio como la unidad básica del Estado y qué implicaciones tiene esto para la participación ciudadana?", "tipo": "abierta"},
        {"texto": "El documento critica la influencia de partidos políticos en los gobiernos municipales. ¿Qué riesgos menciona y cómo afectan a las comunidades? Argumente si está de acuerdo o no.", "tipo": "abierta"},
        {"texto": "¿Qué relación existe entre los COCODE y el COMUDE en la planificación del desarrollo? Explica el flujo de decisiones.", "tipo": "abierta"},
        {"texto": "¿Por qué es importante el presupuesto participativo y qué problemas busca evitar? Incluya un ejemplo concreto.", "tipo": "abierta"},
        {"texto": "¿Por qué se insiste en la inclusión de mujeres y autoridades indígenas dentro del COMUDE?", "tipo": "abierta"},
        {"texto": "¿Qué funciones tiene el COMUDE en la planificación, ejecución y evaluación de proyectos municipales? Organice su respuesta en las tres etapas.", "tipo": "abierta"},
        {"texto": "Desde una perspectiva crítica: ¿cuáles son los principales desafíos para que el COMUDE funcione de manera efectiva en la práctica? Proponga al menos dos soluciones.", "tipo": "abierta"},

        {
            "texto": "¿Cuál de las siguientes situaciones refleja mejor el concepto de auditoría social?",
            "tipo": "opcion_multiple",
            "opciones": [
                "El alcalde presenta informes financieros al Ministerio de Finanzas",
                "Una empresa supervisa la ejecución de obras municipales",
                "La comunidad revisa y da seguimiento al uso de recursos públicos",
                "La municipalidad contrata auditores externos"
            ]
        },
        {
            "texto": "¿Por qué se insiste en que el COMUDE debe basarse en la participación de los COCODE?",
            "tipo": "opcion_multiple",
            "opciones": [
                "Para cumplir un requisito legal",
                "Porque los COCODE representan los intereses del alcalde",
                "Porque permiten priorizar necesidades desde las comunidades",
                "Porque facilitan la ejecución técnica de proyectos"
            ]
        },
        {
            "texto": "Una municipalidad utiliza la mayor parte del presupuesto en la cabecera municipal y no en las comunidades rurales, esto evidencia:",
            "tipo": "opcion_multiple",
            "opciones": [
                "Una estrategia de desarrollo urbano",
                "Una correcta priorización de recursos",
                "Una desigualdad en la inversión municipal",
                "Una limitación técnica del municipio."
            ]
        },
    ]

    crear_formulario_con_preguntas(
        apps,
        titulo="DOCUMENTO DE INDUCCIÓN - COMUDE",
        descripcion="En base a la lectura del documento, responda las siguientes preguntas, si se tiene interrogantes sobre el mismo, consulte con el coordinador respectivo para poder ahondar en el análisis.",
        preguntas_data=preguntas
    )


def eliminar_formulario_induccion(apps, schema_editor):
    eliminar_formulario(apps, "DOCUMENTO DE INDUCCIÓN - COMUDE")