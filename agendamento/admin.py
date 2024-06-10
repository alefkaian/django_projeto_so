from django.contrib import admin
from .models import Agendamento
from django.contrib.admin import AdminSite
from django.shortcuts import redirect


# Register your models here.


class AgendamentoAdmin(admin.ModelAdmin):
    list_display = (
        "nome_do_tutor",
        "nome_do_animal",
        "tipo_de_animal",
        "data",
        "horario",
    )


admin.site.register(Agendamento, AgendamentoAdmin)
