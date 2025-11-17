from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rrhh.models import Usuario
from rrhh.serializers import UsuarioSerializer
from rrhh.models_token import AuthToken
import secrets

@api_view(['POST'])
@permission_classes([AllowAny])
def login_usuario(request):
    username = request.data.get("nombreusuario")
    password = request.data.get("contrasena")

    try:
        usuario = Usuario.objects.get(nombreusuario=username)
    except Usuario.DoesNotExist:
        return Response({"success": False, "message": "Usuario no existe"}, status=400)

    if not usuario.estado:
        return Response({"success": False, "message": "Usuario inactivo"}, status=403)

    if not check_password(password, usuario.contrasena):
        return Response({"success": False, "message": "Contraseña incorrecta"}, status=400)

    # 🔐 Generar o recuperar token
    token, _ = AuthToken.objects.get_or_create(usuario=usuario)

    # 🔥 Si no tiene key, generarla
    if not token.key:
        token.key = secrets.token_hex(20)
        token.save()

    serializer = UsuarioSerializer(usuario)

    return Response({
        "success": True,
        "token": token.key,
        "usuario": serializer.data
    })
