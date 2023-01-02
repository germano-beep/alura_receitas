from django.contrib import admin
from .models import Pessoa

class ListandoPessoas(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email')
    search_fields = ('nome',)
    list_display_links = ('id', 'nome')
    list_per_page = 2

admin.site.register(Pessoa, ListandoPessoas)