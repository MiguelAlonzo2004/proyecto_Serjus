from django.db import models
from rrhh.models import Usuario

class AuthToken(models.Model):
    key = models.CharField(max_length=40, unique=True, db_index=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auth_token"
