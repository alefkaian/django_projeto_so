from .models import Agendamento
from datetime import timedelta
from babel.dates import format_date
from django.utils import timezone

def gerar_horarios_indisponiveis():
    agendamentos = (
        Agendamento.objects.filter(data__gte=timezone.localtime().date())
        .exclude(horario=None)
        .values("data", "horario", "tipo_de_agendamento")
    )

    horarios_indisponiveis = {}

    for agendamento in agendamentos:
        data = agendamento["data"].strftime("%Y-%m-%d")
        horario = agendamento["horario"].strftime("%H:%M")
        tipo_de_agendamento = agendamento["tipo_de_agendamento"]

        if data not in horarios_indisponiveis:
            horarios_indisponiveis[data] = {
                "horario_14": False,
                "horario_15": False,
                "horario_16": False,
                "horario_17": False,
            }

        # Se o tipo de agendamento for Cirurgia, marcar todos os horários como indisponíveis
        if tipo_de_agendamento == "Cirurgia":
            horarios_indisponiveis[data] = {
                "horario_14": True,
                "horario_15": True,
                "horario_16": True,
                "horario_17": True,
            }
        else:
            if horario == "14:00":
                horarios_indisponiveis[data]["horario_14"] = True
            elif horario == "15:00":
                horarios_indisponiveis[data]["horario_15"] = True
            elif horario == "16:00":
                horarios_indisponiveis[data]["horario_16"] = True
            elif horario == "17:00":
                horarios_indisponiveis[data]["horario_17"] = True

    return [
        {"data": data, **horarios} for data, horarios in horarios_indisponiveis.items()
    ]



def has_substring_after(main_string, sub_string):
    # Encontra a posição inicial da substring na string principal
    position = main_string.find(sub_string)

    # Se a substring não for encontrada, retorna False
    if position == -1:
        return False

    # Calcula a posição onde a substring termina
    end_position = position + len(sub_string)

    # Verifica se há algo depois da posição final da substring
    return end_position < len(main_string)

def get_week_dates(today):
    week_date_0 = today - timedelta(days=today.weekday())
    week_dates = [week_date_0 + timedelta(days=i) for i in range(5)]
    return week_dates

def get_agendamentos_week_dates(agendamento_list, week_dates):
    agendamentos_week_dates = [
        (
            format_date(date, format="d MMM", locale="pt_BR"),
            agendamento_list.filter(data=date).order_by("horario"),
        )
        for date in week_dates
    ]
    return agendamentos_week_dates