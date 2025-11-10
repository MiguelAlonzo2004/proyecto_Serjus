# rrhh/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from datetime import datetime, date
from django.contrib.auth.hashers import make_password
from .models import Usuario, Rol, Empleado, Tipodocumento, Tipoevaluacion, Estado, Variable, Criterio


@receiver(post_migrate)
def create_default_admin_and_data(sender, **kwargs):
    """
    Crea datos por defecto después de aplicar migraciones en la app rrhh.
    Incluye usuario admin, tipos de documentos, tipos de evaluación, estados base y variables específicas por tipo.
    """
    if sender.name != "rrhh":
        return

    # === Crear rol Administrador ===
    rol_admin, _ = Rol.objects.get_or_create(
        nombrerol="Administrador",
        defaults={
            'descripcion': 'Rol con todos los permisos',
            'estado': True,
            'idusuario': 1,
        }
    )

    # === Crear empleado por defecto ===
    empleado_default, _ = Empleado.objects.get_or_create(
        dpi="0000000000000",
        defaults={
            'nit': "0000000",
            'nombre': "Empleado",
            'apellido': "Default",
            'genero': "Otro",
            'lugarnacimiento': "Ciudad Default",
            'fechanacimiento': date(1990, 1, 1),
            'telefonocelular': "0000000000",
            'telefonoresidencial': None,
            'telefonoemergencia': None,
            'email': "admin@example.com",
            'direccion': "Dirección Default",
            'estadocivil': "Soltero",
            'numerohijos': 0,
            'idusuario': 1,
            'estado': True
        }
    )

    # === Crear usuario admin ===
    if not Usuario.objects.filter(nombreusuario="admin").exists():
        Usuario.objects.create(
            nombreusuario="admin",
            contrasena=make_password("admin123"),
            estado=True,
            createdat=datetime.now(),
            updatedat=datetime.now(),
            idrol=rol_admin,
            idempleado=empleado_default
        )
        print("Usuario admin creado correctamente.")

    # === Tipos de documentos por defecto ===
    documentos_por_defecto = [
        "CURRICULUM ACREDITADO",
        "INFORME",
        "COMPROBANTE DE AUSENCIA",
        "LLAMADAS DE ATENCIÓN",
        "DOCUMENTOS DE INDUCCIÓN",
        "CONTRATO",
        "RECONOCIMIENTO",
    ]
    for nombre in documentos_por_defecto:
        Tipodocumento.objects.get_or_create(
            nombretipo=nombre,
            defaults={'descripcion': nombre, 'estado': True, 'idusuario': 1}
        )
    print("Tipos de documentos creados correctamente.")

    # === Tipos de evaluación por defecto ===
    tipos_evaluacion = ["Coordinador", "Acompañante", "Administrativo", "Entrevista"]
    tipos_creados = {}
    for tipo in tipos_evaluacion:
        t, _ = Tipoevaluacion.objects.get_or_create(
            nombretipo=tipo,
            defaults={'estado': True, 'idusuario': 1}
        )
        tipos_creados[tipo] = t
    print("Tipos de evaluación creados correctamente.")

    # === Estados por defecto ===
    estados_aspirantes = [
        {"nombreestado": "Postulado", "descripcion": "Aspirante ha postulado"},
        {"nombreestado": "Seleccionado para Entrevista", "descripcion": "Aspirante seleccionado para entrevista"},
        {"nombreestado": "Rechazado", "descripcion": "Aspirante no continúa en el proceso"},
    ]
    estados_convocatorias = [
        {"nombreestado": "Abierta", "descripcion": "Convocatoria disponible para postulaciones activas."},
        {"nombreestado": "Cerrada", "descripcion": "Convocatoria cerrada. No se aceptan nuevas postulaciones."},
        {"nombreestado": "Finalizada", "descripcion": "Convocatoria finalizada. Se completó el proceso de selección."},
        {"nombreestado": "Contratado", "descripcion": "Aspirante ha sido contratado"},
    ]
    todos_los_estados = estados_aspirantes + estados_convocatorias
    for e in todos_los_estados:
        Estado.objects.get_or_create(
            nombreestado=e["nombreestado"],
            defaults={'descripcion': e["descripcion"], 'estado': True, 'idusuario': 1}
        )
    print("Estados base creados correctamente.")

    # === Variables específicas por tipo de evaluación ===
    variables_por_tipo = {
        "Coordinador": [
            "Información - Comunicación Interna",
            "Toma De Decisiones",
            "Planteamiento Estrategico",
            "Desarrollo Del Personal y Trabajo En Equipo",
            "Motivación",
            "Administración",
            "Identidad",
            "Cooperación E Integridad",
        ],
        "Administrativo": [
            "Calidad y eficiencia",
            "Compromiso y presentación",
            "Trabajo en equipo",
        ],
        "Acompañante": [
            "Componente Tecnico",
            "Componente Politico-Metodologico",
            "Componente Personal",
        ],
    }

    for tipo_nombre, variables in variables_por_tipo.items():
        tipo = tipos_creados.get(tipo_nombre)
        if not tipo:
            print(f"No se encontró tipo de evaluación {tipo_nombre}")
            continue

        for v in variables:
            variable, creada = Variable.objects.get_or_create(
                idtipoevaluacion=tipo,
                nombrevariable=v,
                defaults={"estado": True, "idusuario": 1}
            )
            if creada:
                print(f"Variable creada: {v} ({tipo_nombre})")

    print("Variables específicas por tipo creadas correctamente.")
    
     # === CRITERIOS BASE PARA COORDINADORES ===
    tipo_coord = tipos_creados.get("Coordinador")
    if tipo_coord:
        # Buscar o crear variables del tipo "Coordinador"
        variables_coord = {
            v.nombrevariable: v
            for v in Variable.objects.filter(idtipoevaluacion=tipo_coord)
        }

        criterios_por_variable = {
            "Información - Comunicación Interna": [
                "Busca, analiza y distribuye información al equipo",
                "Procura recibir la mayor cantidad de información, especialmente de los propios miembros del equipo",
                "Demuestra receptividad a la opinión de los miembros del equipo, valora las opiniones y percepciones.",
                "Crea mecanismos de retroalimentación entre todos los miembros del equipo.",
                "Establece instancias o mecanismos (reuniones, envío de correo electrónico, etc.) para intercambio continuo de información.",
                "Es transparente en el manejo de información de utilidad para el equipo.",
                "Traslada la información del equipo a otras instancias de dirección o decisión",
                "Busca y promueve mecanismos de comunicación para reducir problemas, dificultades, conflictos",
                "Se comunica de manera asertiva, logra dar los mensajes en forma eficaz y eficiente",
            ],
            "Toma De Decisiones": [
                "Establece o ayuda a establecer guías o parámetros para tomar decisiones, es decir todos en su equipo saben 'quién puede decidir qué'",
                "Ayuda al equipo a aprender a tomar decisiones, poco a poco, en asuntos cada vez más relevantes.",
                "Motiva a tomar riesgos, a atreverse a resolver asuntos, a adoptar una actitud de solución de problemas y de aprovechamiento de oportunidades.",
                "Conoce las decisiones que pueden tomar los miembros del equipo según el nivel de información que cada persona posee y necesita.",
            ],
            "Planteamiento Estrategico": [
                "Procura el mayor involucramiento del personal en relación a la estrategia institucional, desde su formulación y aplicación.",
                "Influye en el personal, para que los miembros del equipo reconozcan su papel activo en los resultados y procesos internos.",
                "Asegura que el personal cuente con las capacidades para implementar el planteamiento estratégico institucional.",
                "Promueve en el personal la disposición de sugerir, comentar y crear ideas en relación al plan de trabajo y al planteamiento estratégico de la institución.",
                "Comparte la visión de la institución con su equipo.",
                "Impulsa un seguimiento del desarrollo de la estrategia institucional con los miembros de su equipo.",
                "Promueve en el equipo a 'pensar estratégicamente' con visión de futuro.",
                "Promueve el análisis del contexto y su relación con la estrategia y propuesta institucional.",
                "Conoce, aplica y orienta al equipo sobre la apuesta política y propuestas estratégicas de la institución.",
                "Promueve en el equipo la relación o vinculación de los procesos (lo micro con lo macro y sectorial con lo territorial).",
                "En la revisión y orientación de estrategias, planes, documentos, diseños, verifica que integren la CMD, la POP, democracia en género y el PPA para avanzar en la construcción del Estado Plurinacional.",
                "Conoce y orienta el tipo de alianzas que se están estableciendo desde los procesos a su cargo.",
            ],
            "Desarrollo Del Personal y Trabajo En Equipo": [
                "Fomenta el aprendizaje del equipo en diversas temáticas relacionadas a los procesos que se acompañan.",
                "Busca nuevas maneras para mejorar el desarrollo del personal, procurando innovaciones que logren impacto.",
                "Promueve orden, coordinación e integración de los miembros al interno del equipo y con los otros equipos.",
                "Desarrolla capacidad de los miembros del equipo para realizar tareas que anteriormente el coordinador asumía como responsabilidad propia y única.",
                "Prepara al equipo para que participen y funcionen como sistema.",
                "Promueve al equipo para que satisfagan necesidades profesionales y técnicas, para mejorar la calidad del trabajo.",
                "Conoce, transmite y orienta al equipo en temas técnicos, operativos, de funcionamiento, políticos y metodológicos, para el alcance de objetivos dentro de los procesos.",
            ],
            "Motivación": [
                "Fomenta que el personal sienta orgullo por lo que hace.",
                "Promueve que la organización aprecie del equipo, sus individualidades, talentos especiales, para cumplir las responsabilidades con confianza y seguridad.",
                "Conoce, aprende o trata de implementar procesos de motivación al equipo.",
                "Demuestra motivación en las acciones que realiza.",
            ],
            "Administración": [
                "Cuenta con capacidad para seleccionar y aportar en el proceso de inducción de personal nuevo.",
                "Tiene claridad del normativo interno para otorgar permisos, autorizaciones y sanciones al personal a su cargo.",
                "Vela por el cumplimiento de políticas institucionales y de las funciones del equipo a su cargo.",
                "Supervisa, apoya y asesora el desempeño del personal a su cargo.",
                "Monitorea permanentemente la ejecución presupuestaria de los proyectos a su cargo para evitar sobre o sub ejecución.",
                "Elabora, gestiona y le aprueban proyectos para cubrir las necesidades del proceso a su cargo, integrando lo establecido en la política de democracia en género y los PPA.",
                "Elabora informes para las agencias, en tiempo y con calidad para ser revisados.",
                "Maneja adecuadamente múltiples demandas y prioridades.",
            ],
            "Identidad": [
                "Demuestra de forma constante y consistente compromiso personal con SERJUS.",
                "Comprende y está comprometido con la estructura, funcionamiento y apuesta de SERJUS.",
                "Muestra iniciativa, cooperación y creatividad para aportar tanto a lo interno de SERJUS como en el proceso a su cargo.",
                "Es confiable, cumple con fechas establecidas, acuerdos y compromisos.",
                "Rechaza y denuncia cualquier acto de acoso o violencia hacia las mujeres.",
                "Lidera el proceso con claridad, confianza, aprecio y generando relaciones de poder democráticas, con equidad y justicia.",
                "Promueve los principios y valores de SERJUS los cuales son visibles tanto fuera como dentro de SERJUS.",
            ],
            "Cooperación E Integridad": [
                "Demuestra cooperación, solidaridad y honestidad en sus relaciones laborales.",
                "Actúa con coherencia ética en sus decisiones y acciones.",
                "Fomenta la transparencia y la rendición de cuentas dentro de su equipo.",
                "Contribuye a mantener un ambiente de respeto, equidad y apoyo mutuo.",
            ],
        }

        for nombre_variable, criterios in criterios_por_variable.items():
            variable = variables_coord.get(nombre_variable)
            if not variable:
                print(f"⚠️ Variable no encontrada para criterios: {nombre_variable}")
                continue

            for c in criterios:
                _, creada = Criterio.objects.get_or_create(
                    idvariable=variable,
                    nombrecriterio=c,
                    defaults={
                        "descripcioncriterio": "Criterio institucional de evaluación para coordinadores.",
                        "estado": True,
                        "idusuario": 1,
                    },
                )
                if creada:
                    print(f"Criterio creado: {c} → {nombre_variable}")

    print("Criterios base de Coordinadores creados correctamente.")
    
        # === CRITERIOS BASE PARA ADMINISTRATIVOS ===
    tipo_admin = tipos_creados.get("Administrativo")
    if tipo_admin:
        variables_admin = {
            v.nombrevariable: v
            for v in Variable.objects.filter(idtipoevaluacion=tipo_admin)
        }

        criterios_admin_por_variable = {
            "Calidad y eficiencia": [
                "Precisión y calidad del trabajo realizado.",
                "Cantidad de trabajo completado.",
                "Organización del trabajo en tiempo y forma.",
                "Cuidado de herramientas y equipo asignado.",
            ],
            "Conocimiento de Funciones": [
                "Nivel de experiencia y conocimiento técnico para el trabajo requerido.",
                "Uso y conocimiento de procedimientos administrativos establecidos institucionalmente.",
                "Uso y conocimiento de herramientas e instrumentos administrativos institucionales.",
                "Puede desempeñarse con poca o ninguna ayuda.",
                "Capacidad de enseñar o explicar a otras personas los procedimientos a realizar.",
                "Conocimiento de la institución y de las funciones a desarrollar en el puesto definido.",
            ],
            "Compromiso y presentación": [
                "Trabaja sin necesidad de monitoreo o supervisión.",
                "Se esfuerza más si la situación lo requiere.",
                "Puntualidad, en oficina y en los procesos.",
                "Presentación rápida y ordenada de lo que se le solicita.",
            ],
            "Trabajo en equipo": [
                "Trabaja fluidamente con acompañantes, personal administrativo y coordinaciones.",
                "Tiene una actitud positiva y proactiva.",
                "Promueve el trabajo en equipo y la coordinación.",
            ],
        }

        for nombre_variable, criterios in criterios_admin_por_variable.items():
            variable = variables_admin.get(nombre_variable)
            if not variable:
                print(f"Variable no encontrada para criterios administrativos: {nombre_variable}")
                continue

            for c in criterios:
                _, creada = Criterio.objects.get_or_create(
                    idvariable=variable,
                    nombrecriterio=c,
                    defaults={
                        "descripcioncriterio": "Criterio institucional de evaluación para personal administrativo.",
                        "estado": True,
                        "idusuario": 1,
                    },
                )
                if creada:
                    print(f"Criterio creado (Administrativo): {c} → {nombre_variable}")

    print("Criterios base de Administrativos creados correctamente.")
    
        # ===  CRITERIOS BASE PARA ACOMPAÑANTES ===
    tipo_acomp = tipos_creados.get("Acompañante")
    if tipo_acomp:
        variables_acomp = {
            v.nombrevariable: v
            for v in Variable.objects.filter(idtipoevaluacion=tipo_acomp)
        }

        criterios_acomp_por_variable = {
            "Componente Tecnico": [
                "Conocimiento del Trabajo",
                "Calidad del Trabajo",
                "Eficiencia y Eficacia",
                "Capacidad de Planificar, Monitorear y Evaluar",
                "Capacidad de organizar",
                "Solución de problemas y toma de Decisiones",
                "Comunicación",
                "Capacidad de Asimilación",
                "Redacción",
            ],
            "Componente Politico-Metodologico": [
                "Formación Metodológica",
                "Conocimiento de la Realidad",
                "Identificación con el Planteamiento Institucional",
                "Democracia en género",
                "Vinculación de lo Territorial y Sectorial",
            ],
            "Componente Personal": [
                "Relaciones Interpersonales",
                "Asistencia y Puntualidad",
                "Responsabilidad",
                "Iniciativa",
                "Cooperación",
                "Superación laboral",
            ],
        }

        for nombre_variable, criterios in criterios_acomp_por_variable.items():
            variable = variables_acomp.get(nombre_variable)
            if not variable:
                print(f"Variable no encontrada para criterios de Acompañantes: {nombre_variable}")
                continue

            for c in criterios:
                _, creada = Criterio.objects.get_or_create(
                    idvariable=variable,
                    nombrecriterio=c,
                    defaults={
                        "descripcioncriterio": "Criterio institucional de evaluación para acompañantes.",
                        "estado": True,
                        "idusuario": 1,
                    },
                )
                if creada:
                    print(f"Criterio creado (Acompañante): {c} → {nombre_variable}")

    print("Criterios base de Acompañantes creados correctamente.")

