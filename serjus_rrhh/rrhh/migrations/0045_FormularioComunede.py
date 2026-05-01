from django.db import migrations

# IMPORTAS TODOS
from rrhh.utils.Documentos.Formulario_COMUDE import crear_formulario_induccion, eliminar_formulario_induccion
from rrhh.utils.Documentos.Formulario_PME import crear_formulario_induccion as crear_pme, eliminar_formulario_induccion as eliminar_pme
from rrhh.utils.Documentos.Formulario_Haciendo import crear_formulario_haciendo_realidad, eliminar_formulario_haciendo_realidad
from rrhh.utils.Documentos.Formulario_Proyecto import crear_formulario_proyecto_politico, eliminar_formulario_proyecto_politico
from rrhh.utils.Documentos.Formulario_COCODES import crear_formulario_cocodes_maya, eliminar_formulario_cocodes_maya
from rrhh.utils.Documentos.Formulario_Alcaldia import crear_formulario_alcaldia_indigena, eliminar_formulario_alcaldia_indigena
from rrhh.utils.Documentos.Formulario_Capitalismo import crear_formulario_capitalismo, eliminar_formulario_capitalismo
from rrhh.utils.Documentos.Formulario_Genero import crear_formulario_genero, eliminar_formulario_genero
from rrhh.utils.Documentos.Formulario_Codigo import crear_formulario_codigo_conducta, eliminar_formulario_codigo_conducta
from rrhh.utils.Documentos.Formulario_PlanMultianual import crear_formulario_plan_multianual, eliminar_formulario_plan_multianual
from rrhh.utils.Documentos.Formulario_Reglamento import crear_formulario_reglamento, eliminar_formulario_reglamento


def cargar_todos_los_formularios(apps, schema_editor):
    crear_formulario_induccion(apps, schema_editor)  # COMUDE
    crear_pme(apps, schema_editor)
    crear_formulario_haciendo_realidad(apps, schema_editor)
    crear_formulario_proyecto_politico(apps, schema_editor)
    crear_formulario_cocodes_maya(apps, schema_editor)
    crear_formulario_alcaldia_indigena(apps, schema_editor)
    crear_formulario_capitalismo(apps, schema_editor)
    crear_formulario_genero(apps, schema_editor)
    crear_formulario_codigo_conducta(apps, schema_editor)
    crear_formulario_plan_multianual(apps, schema_editor)   
    crear_formulario_reglamento(apps, schema_editor)        


def eliminar_todos_los_formularios(apps, schema_editor):
    eliminar_formulario_induccion(apps, schema_editor)
    eliminar_pme(apps, schema_editor)
    eliminar_formulario_haciendo_realidad(apps, schema_editor)
    eliminar_formulario_proyecto_politico(apps, schema_editor)
    eliminar_formulario_cocodes_maya(apps, schema_editor)
    eliminar_formulario_alcaldia_indigena(apps, schema_editor)
    eliminar_formulario_capitalismo(apps, schema_editor)
    eliminar_formulario_genero(apps, schema_editor)
    eliminar_formulario_codigo_conducta(apps, schema_editor)
    eliminar_formulario_plan_multianual(apps, schema_editor)  
    eliminar_formulario_reglamento(apps, schema_editor)       
    


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0044_opcion_orden'),
    ]

    operations = [
        migrations.RunPython(cargar_todos_los_formularios, eliminar_todos_los_formularios),
    ]