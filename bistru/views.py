from django.http import HttpResponse
from .models import Estudante, Avaliacao, Historico, Refeicao, Usuario
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta


# Create your views here.
# view de login - precisa receber algum padrão?

def entrar(request):
    # estudante = Estudante.objects
    if request.user.is_authenticated:
        return redirect('bistru:rotas_login')
    
    if request.method == 'POST':
        usuario_form = request.POST.get('email')
        senha_form = request.POST.get('senha')

        # verificando no banco de dados
        user = authenticate(request, email = usuario_form, password=senha_form)

        if user is not None:
            login(request, user)
            return redirect('bistru:rotas_login')
            messages.success(request, 'Login realizado com sucesso')
        else:
            messages.error(request, 'Usuário ou senha inválidos')

    return render(request, 'bistru/login.html')

def sair(request):
    logout(request)
    return redirect('bistru:entrar')

def rotas_login(request):
    if not request.user.is_authenticated:
        return redirect('bistru:entrar')

    if request.user.is_authenticated:
        if request.user.tipo_usuario == Usuario.TipoUsuario.ADMIN:
            return redirect('/admin/')
        else:
            return redirect('bistru:cardapio')
            messages.sucess(request, "Redirecionando para cardápio...")

    return redirect('bistru:entrar')

@login_required(login_url='/login/')
def cardapio(request):
    
    estudante = Estudante.objects.first()
    nome_usuario = estudante.nome if estudante else "Estudante"
    creditos_usuario = estudante.quantidade_creditos if estudante else 0

    # hoje = datetime.now().date()
    hoje = datetime(2026, 8, 17, 0, 0, 0)
    dias_semana_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    dias_disponiveis = []

    for i in range(5):
        data_loop = hoje + timedelta(days=i)
        dia_nome = dias_semana_pt[data_loop.weekday()]
        dias_disponiveis.append({
            'val': data_loop.strftime('%Y-%m-%d'),
            'label': f"{dia_nome}, {data_loop.strftime('%d/%m/%y')}"
        })

    data_selecionada = request.GET.get('data', dias_disponiveis[0]['val'])

    refeicoes_bd = Refeicao.objects.filter(data=data_selecionada)
    refeicoes_formatadas = []

    for ref in refeicoes_bd:
        pratos_lista = []
        if ref.prato_proteico1:
            pratos_lista.append({'categoria': 'Prato Proteico', 'nome': ref.prato_proteico1})
        if ref.prato_proteico2:
            pratos_lista.append({'categoria': 'Prato Proteico', 'nome': ref.prato_proteico2})
        if ref.prato_vegetariano:
            pratos_lista.append({'categoria': 'Opção Vegetariana', 'nome': ref.prato_vegetariano})
        if ref.acompanhamento1:
            pratos_lista.append({'categoria': 'Acompanhamento', 'nome': ref.acompanhamento1})
        if ref.acompanhamento2:
            pratos_lista.append({'categoria': 'Acompanhamento', 'nome': ref.acompanhamento2})
        if ref.sobremesa_fruta:
            pratos_lista.append({'categoria': 'Sobremesa', 'nome': ref.sobremesa_fruta})
        if ref.bebida:
            pratos_lista.append({'categoria': 'Bebida', 'nome': ref.bebida})

        refeicoes_formatadas.append({
            'nome': ref.get_tipo_display(),
            'pratos': pratos_lista
        })

    context = {
        'nome': nome_usuario,
        'creditos': creditos_usuario,
        'dias_disponiveis': dias_disponiveis,
        'data_selecionada': data_selecionada,
        'refeicoes': refeicoes_formatadas,
    }

    return render(request, 'bistru/cardapio.html', context)
    

# @login_required(login_url='/login/')
# def cardapio(request):
#     return render(request, 'bistru/cardapio.html', {'user': request.user})