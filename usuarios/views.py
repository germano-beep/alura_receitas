from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

# Create your views here.
def cadastro(request):
  if request.method == 'POST':
    nome = request.POST['nome']
    email = request.POST['email']
    senha = request.POST['password']
    senha2 = request.POST['password2']

    if not empty_field(nome):
      print("Campo inválido. Digite seu nome corretamente.")
      return render(request, 'usuarios/cadastro.html')
    if not empty_field(email):
      print("Escreva o campo email corretamente")
      return render(request, 'usuarios/cadastro.html')
    if senha != senha2:
      messages.error(request, 'Senhas não iguais.')
      return render(request, 'usuarios/cadastro.html')
    if User.objects.filter(email=email).exists():
      messages.error(request, 'Usuário já cadastrado')
      return render(request, 'usuarios/cadastro.html')

    user = User.objects.create_user(username=nome, email=email, password=senha)
    user.save()

    messages.success(request, 'Cadastro realizado com sucesso')
    return redirect('login')
  else:
    return render(request, 'usuarios/cadastro.html')

def login(request):
  if request.method == 'POST':
    email = request.POST['email']
    senha = request.POST['senha']

    if empty_field(email) or empty_field(senha):
      messages.error(request, 'Campo email e senha não podem estar vazios.')
      return redirect('login')
    
    if User.objects.filter(email=email).exists():
      nome = User.objects.filter(email=email).values_list('username', flat=True)
      print(f'nome do usuário{nome}')
      user = auth.authenticate(username=nome[0], password=senha)
      print(nome)

      if user is not None:
        auth.login(request, user)
        return redirect('dashboard')

      return redirect('login')
    
    else:
      messages.error(request, 'Usuário ou senha errado')
      return redirect('login')

    
  return render(request, 'usuarios/login.html')

def logout(request):
  auth.logout(request)
  return redirect('index')

def dashboard(request):
  if request.user.is_authenticated:
    id = request.user.id
    receitas = Receita.objects.order_by('-date_receita').filter(pessoa=id)

    dados = {
      'receitas': receitas
    }

    return render(request, 'usuarios/dashboard.html', dados)
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

  return render(request, 'usuarios/cria_receita.html')

def empty_field(field):
  return field.strip()

def different_passwords(password, password2):
  return password != password2
