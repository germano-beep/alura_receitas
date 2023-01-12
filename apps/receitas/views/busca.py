from django.shortcuts import render
from receitas.models import Receita

def busca(request):
  lista_receitas = Receita.objects.order_by('-date_receita').filter(publicada=True)
  print(lista_receitas)
  if 'search' in request.GET:
    nome_a_busca = request.GET['search']
    if busca:
      receitas = lista_receitas.filter(nome_receita__icontains=nome_a_busca)

    dados = {
      "receitas": receitas
    }
  return render(request, 'receitas/busca.html', dados)