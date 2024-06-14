from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from .forms import AgendamentoForm, AgendamentoFormAdm
from .models import Agendamento
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import Group
from django.contrib.auth import logout as auth_logout
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from json import dumps
from babel.dates import format_date
from rest_framework import viewsets
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from .serializers import AgendamentoSerializer
from .aux_views import gerar_horarios_indisponiveis, has_substring_after, get_week_dates, get_agendamentos_week_dates


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


def sucesso(request):
    if request.user.is_authenticated:
        base_template = 'agendamento/base_admin.html'
    else:
        base_template = 'agendamento/base.html'
    context = {
        'base_template': base_template
    }
    previous_url = None
    referer = request.META.get("HTTP_REFERER")
    if referer:
        previous_url = referer
    if not request.session.get("form_submitted"):
        return HttpResponseForbidden("Acesso proibido")
    request.session["form_submitted"] = False
    if has_substring_after(previous_url, "/agendar/"):
        return render(request, "agendamento/sucesso_editar.html", context)
    else:
        return render(request, "agendamento/sucesso.html", context)



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser: # type: ignore
                return redirect("admin:index")
            elif (
                Group.objects.get(name="Gerenciamento")
                .user_set.filter(id=user.id) # type: ignore
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


@login_required # type: ignore
def editar_agendamentos(request, periodo):
    match periodo:
        case 0:
            return render(request, "agendamento/editar_agendamentos.html", {"periodo": "Sem Data"})
        case 1:
            return render(request, "agendamento/editar_agendamentos.html", {"periodo": "Futuros"})
        case -1:
            return render(request, "agendamento/editar_agendamentos.html", {"periodo": "Antigos"})

@login_required
def agendamentos_sem_data(request):
    context = {"agendamentos_sem_data": Agendamento.objects.filter(data__isnull=True).order_by('data_de_criacao')}
    return render(request, "agendamento/agendamentos_sem_data.html", context)



class ReqAgendamentosFuturos(viewsets.ModelViewSet):
    queryset = Agendamento.objects.filter(data__gte=datetime.now().date())
    serializer_class = AgendamentoSerializer


class ReqAgendamentosAntigos(viewsets.ModelViewSet):
    queryset = Agendamento.objects.filter(data__lt=datetime.now().date())
    serializer_class = AgendamentoSerializer


class ReqAgendamentosSemData(viewsets.ModelViewSet):
    queryset = Agendamento.objects.filter(data__isnull=True)
    serializer_class = AgendamentoSerializer

class ReqAgendamentosDia(viewsets.ModelViewSet):
    serializer_class = AgendamentoSerializer
    def get_queryset(self):
        data_especifica = self.request.query_params.get('dia', None) # type: ignore
        if data_especifica is not None and data_especifica != '':
            print(parse_datetime(data_especifica))
            queryset = Agendamento.objects.filter(data=parse_datetime(data_especifica).date()).order_by('horario') # type: ignore
        else:
            queryset = Agendamento.objects.none()

        return queryset
    
class ReqAgendamentoHorario(viewsets.ModelViewSet):
    serializer_class = AgendamentoSerializer

    def get_queryset(self):
        dia_especifico = self.request.query_params.get('dia', None) # type: ignore
        hora_especifica = self.request.query_params.get('hora', None) # type: ignore

        if dia_especifico is not None and dia_especifico != '' and hora_especifica is not None and hora_especifica != '':
            data_hora = parse_datetime(f"{dia_especifico} {hora_especifica}")
            queryset = Agendamento.objects.filter(
                Q(data=data_hora.date(), horario=data_hora.time()) | # type: ignore
                (Q(tipo_de_agendamento="Cirurgia") & Q(data=data_hora.date())) # type: ignore
            )
        else:
            queryset = Agendamento.objects.none()

        return queryset

def redirect_root(request):
    return redirect("agendar")


def teste(request):
    context = {"agendamentos_sem_data": Agendamento.objects.filter(data__isnull=True).order_by('data_de_criacao')}
    return render(request, "agendamento/sem_data.html", context)
