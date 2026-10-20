from django.contrib import admin

# Register your models here.
from .models import Avaliacao, Estudante, Refeicao, Historico

admin.site.register(Avaliacao)
admin.site.register(Estudante)
admin.site.register(Refeicao)
admin.site.register(Historico)