from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class UsuarioManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("O usuário deve possuir um e-mail.")
        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("tipo_usuario", Usuario.TipoUsuario.ADMIN)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    username = None

    email = models.EmailField(unique=True)

    class TipoUsuario(models.TextChoices):
        ADMIN = "AD", "Administrador"
        ESTUDANTE = "ES", "Estudante"

    tipo_usuario = models.CharField(
        max_length=2,
        choices=TipoUsuario.choices,
        default=TipoUsuario.ESTUDANTE
    )
    objects = UsuarioManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Estudante(models.Model):
    class TipoAcesso(models.TextChoices):
        P1 = "P1", _("Prioridade 1")
        COMEXT = "CE", _("Comunidade externa")
        COMIN = "CI", _("Comunidade interna")

    usuario = models.OneToOneField(
        "bistru.Usuario",
        on_delete=models.CASCADE,
        related_name="dados_estudante"
    )

    nome = models.CharField(max_length=100)
    quantidade_creditos = models.PositiveIntegerField(default=0)
    vinculo_ativo = models.BooleanField(default=True)
    modalidade = models.CharField(max_length=2, choices=TipoAcesso.choices, default=TipoAcesso.COMIN)
    inicio_curso = models.DateField()
    foto_perfil = models.ImageField(upload_to="fotos_perfil/", blank=True, null=True)
    

    def __str__(self):
        return f'{self.nome}, {self.modalidade}'

class Refeicao(models.Model):
    class TipoRefeicao(models.TextChoices):
            ALMOCO = "AL", _("Almoço")
            CAFE = "CA", _("Café da manhã")
            JANTAR = "JA",_("Jantar")

    prato_proteico1 = models.TextField(max_length=50)
    prato_proteico2 = models.TextField(max_length=50, null=True, blank=True)
    prato_vegetariano = models.TextField(max_length=50)
    acompanhamento1 = models.TextField(max_length=50)
    acompanhamento2 = models.TextField(max_length=50)
    acompanhamento3 = models.TextField(null=True, blank=True)
    sobremesa_fruta = models.TextField(max_length=50)
    salada = models.TextField(null=True, blank=True)
    guarnicao = models.TextField(null=True, blank=True)
    molho = models.TextField(null=True, blank=True)
    bebida = models.TextField(max_length=50)
    data = models.DateField()
    tipo = models.CharField(max_length=2, choices=TipoRefeicao.choices)
    cafe = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.TipoRefeicao(self.tipo).label} de {self.data}'

# registro de consumo ?
class Historico(models.Model):
    
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    creditos = models.PositiveIntegerField(default=0)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.estudante.nome} - {self.creditos} - {self.data}'

class Avaliacao(models.Model):
    refeicao = models.ForeignKey(Refeicao, on_delete=models.CASCADE)
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    escalaSatisfacao = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    descricao = models.TextField(max_length = 100, null=True, blank=True)

    def __str__(self):
        return f'{self.escalaSatisfacao} - {self.refeicao.TipoRefeicao(self.refeicao.tipo).label} - {self.data} - {self.estudante.nome}'
