from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name = 'index'),
  path('<int:receita_id>', views.receita, name = 'receita'),
  path('busca', views.busca, name = 'busca'),
  path('dashboard', views.dashboard, name='dashboard'),
  path('cria/receita', views.cria_receita, name='cria_receita'),
  path('deleta_receita/<int:receita_id>', views.deleta_receita, name='deleta_receita'),
  path('edita_receita/<int:receita_id>', views.edita_receita, name='edita_receita'),
  path('atualiza_receita', views.atualiza_receita, name='atualiza_receita'),
]