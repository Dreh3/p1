from django.urls import path

from . import views

app_name = 'bistru'

urlpatterns = [
    path("", views.entrar, name="bistru"),
    path('entrar/', views.entrar, name='entrar'),
    path('cardapio/', views.cardapio, name='cardapio'),
    path("redirecionar/", views.rotas_login, name="rotas_login"),
    path("sair/", views.sair, name="sair")

]