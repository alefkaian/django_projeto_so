from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from .forms import AgendamentoForm, AgendamentoFormAdm
from .models import Agendamento
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from json import dumps
from babel.dates import format_date
from rest_framework import viewsets
from .serializers import AgendamentoSerializer
from django.core.paginator import Paginator
from django.urls import reverse


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


def agendar(request, id=None):
    previous_url = None
    referer = request.META.get("HTTP_REFERER")
    if referer:
        previous_url = referer

    agendamento = get_object_or_404(Agendamento, pk=id) if id else None
    agendamento = None if not request.user.is_authenticated else agendamento

    if request.method == "POST":
        form_cls = (
            AgendamentoFormAdm if request.user.is_authenticated else AgendamentoForm
        )
        form = form_cls(request.POST, instance=agendamento)

        if form.is_valid():
            form.save()
            request.session["form_submitted"] = True
            return redirect("sucesso")
    else:
        instance = agendamento if agendamento else None
        form_cls = (
            AgendamentoFormAdm if request.user.is_authenticated else AgendamentoForm
        )
        form = form_cls(instance=instance)

    horarios_indisponiveis = gerar_horarios_indisponiveis()

    if request.user.is_authenticated:
        template = "agendamento/agendar_admin.html"
    else:
        template = "agendamento/agendar.html"

    return render(
        request,
        template,
        {
            "form": form,
            "horarios_indisponiveis": dumps(
                horarios_indisponiveis, cls=DjangoJSONEncoder
            ),
            "previous_url": previous_url,
        },
    )


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


def sucesso(request):
    previous_url = None
    referer = request.META.get("HTTP_REFERER")
    if referer:
        previous_url = referer
    if not request.session.get("form_submitted"):
        return HttpResponseForbidden("Acesso proibido")
    request.session["form_submitted"] = False
    if has_substring_after(previous_url, "/agendar/"):
        return render(request, "agendamento/sucesso_editar.html")
    else:
        return render(request, "agendamento/sucesso.html")


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


def teste(request):
    agendamento_list = Agendamento.objects.order_by("data", "horario").all()
    today = datetime.now()

    week_offset = int(request.GET.get("week_offset", 0))

    today += timedelta(weeks=week_offset)

    week_dates = get_week_dates(today)
    agendamentos_week_dates = get_agendamentos_week_dates(agendamento_list, week_dates)

    context = {
        "agendamentos_week_dates": agendamentos_week_dates,
        "current_year": week_dates[0].strftime("%Y"),
        "current_date": format_date(
            datetime.now().date(), format="d MMM", locale="pt_BR"
        ),
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        cabecalho_html = loader.render_to_string(
            "agendamento/cabecalho_dashboard.html", context
        )
        agendamentos_html = loader.render_to_string(
            "agendamento/conteudo_dashboard.html", context
        )
        return JsonResponse(
            {"cabecalho_html": cabecalho_html, "agendamentos_html": agendamentos_html}
        )

    return render(request, "agendamento/teste.html", context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect("admin:index")
            elif (
                Group.objects.get(name="Gerenciamento")
                .user_set.filter(id=user.id)
                .exists()
            ):
                return redirect("dashboard")
        else:
            return render(
                request, "agendamento/login.html", {"error": "Credenciais inválidas"}
            )
    return render(request, "agendamento/login.html")


def logout(request):
    auth_logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    agendamento_list = Agendamento.objects.order_by("data", "horario").all()
    today = datetime.now()

    week_offset = int(request.GET.get("week_offset", 0))

    today += timedelta(weeks=week_offset)

    week_dates = get_week_dates(today)
    agendamentos_week_dates = get_agendamentos_week_dates(agendamento_list, week_dates)

    context = {
        "agendamentos_week_dates": agendamentos_week_dates,
        "current_year": week_dates[0].strftime("%Y"),
        "current_date": format_date(
            datetime.now().date(), format="d MMM", locale="pt_BR"
        ),
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        cabecalho_html = loader.render_to_string(
            "agendamento/cabecalho_dashboard.html", context
        )
        agendamentos_html = loader.render_to_string(
            "agendamento/conteudo_dashboard.html", context
        )
        return JsonResponse(
            {"cabecalho_html": cabecalho_html, "agendamentos_html": agendamentos_html}
        )

    return render(request, "agendamento/dashboard.html", context)


@login_required
def editar_agendamentos_futuros(request):
    return render(request, "agendamento/editar_agendamentos_futuros.html")


@login_required
def editar_agendamentos_antigos(request):
    return render(request, "agendamento/editar_agendamentos_antigos.html")


@login_required
def editar_agendamentos_semdata(request):
    return render(request, "agendamento/editar_agendamentos_semdata.html")


@login_required
def tabela_ajax(request):
    agendamentos = Agendamento.objects.all()
    paginator = Paginator(agendamentos, 10)  # 10 objetos por página

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    serializer = AgendamentoSerializer(page_obj, many=True)
    return JsonResponse(serializer.data, safe=False)


class ReqAgendamentosFuturos(viewsets.ModelViewSet):
    queryset = Agendamento.objects.filter(data__gte=datetime.now().date())
    serializer_class = AgendamentoSerializer


class ReqAgendamentosAntigos(viewsets.ModelViewSet):
    queryset = Agendamento.objects.filter(data__lt=datetime.now().date())
    serializer_class = AgendamentoSerializer


class ReqAgendamentosSemData(viewsets.ModelViewSet):
    queryset = Agendamento.objects.filter(data__isnull=True)
    serializer_class = AgendamentoSerializer


def redirect_root(request):
    return redirect("agendar")
