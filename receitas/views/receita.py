from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from receitas.models import Receita
from django.contrib.auth.models import User

def index(request):
    receitas = Receita.objects.order_by('-date_receita').filter(publicada=True)

    dados = {
      'receitas' : receitas
    }
    
    return render(request ,'index.html', dados)

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_exibir = {
      'receita': receita    
    }
    return render(request, 'receitas/receita.html', receita_a_exibir)

def dashboard(request):
  if request.user.is_authenticated:
    id = request.user.id
    receitas = Receita.objects.order_by('-date_receita').filter(pessoa=id)

    dados = {
      'receitas': receitas
    }

    return render(request, 'receitas/dashboard.html', dados)
  else:
    return redirect('index')

def cria_receita(request):
  if request.method == 'POST':
    nome_receita = request.POST['nome_receita']
    ingredientes = request.POST['ingredientes']
    modo_preparo = request.POST['modo_preparo']
    tempo_preparo = request.POST['tempo_preparo']
    rendimento = request.POST['rendimento']
    categoria = request.POST['categoria']
    foto_receita = request.FILES['foto_receita']

    user = get_object_or_404(User, pk=request.user.id)
    receita = Receita(pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes, 
                      modo_preparo=modo_preparo, tempo_preparo=tempo_preparo, rendimento=rendimento, 
                      categoria=categoria, foto_receita=foto_receita)

    receita.save()
    return redirect('dashboard')

  return render(request, 'receitas/cria_receita.html')

def deleta_receita(request, receita_id):
  receita = get_object_or_404(Receita, pk=receita_id)
  receita.delete()
  return redirect('dashboard')

def edita_receita(request, receita_id):
  receita = get_object_or_404(Receita, pk=receita_id)
  receita_a_editar = { 'receita': receita }
  return render(request, 'receitas/edita_receita.html', receita_a_editar)

def atualiza_receita(request):
  if request.method == 'POST':
    receita_id = request.POST['receita_id']
    r = get_object_or_404(Receita, pk=receita_id)
    r.nome_receita = request.POST['nome_receita']
    r.ingredientes = request.POST['ingredientes']
    r.modo_preparo = request.POST['modo_preparo']
    r.tempo_preparo = request.POST['tempo_preparo']
    r.rendimento = request.POST['rendimento']
    r.categoria = request.POST['categoria']

    if 'foto_receita' in request.FILES:
      r.foto_receita = request.FILES['foto_receita']

    r.save()

    return redirect('dashboard')
