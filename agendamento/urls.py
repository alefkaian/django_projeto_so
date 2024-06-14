from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(
    r"req_agendamentos_futuros",
    views.ReqAgendamentosFuturos,
    basename="req_agendamentos_futuros",
)
router.register(
    r"req_agendamentos_antigos",
    views.ReqAgendamentosAntigos,
    basename="req_agendamentos_antigos",
)
router.register(
    r"req_agendamentos_semdata",
    views.ReqAgendamentosSemData,
    basename="req_agendamentos_semdata",
)
router.register(
    r"req_agendamentos_dia",
    views.ReqAgendamentosDia,
    basename="req_agendamentos_dia",
)
router.register(
    r"req_agendamento_horario",
    views.ReqAgendamentoHorario,
    basename="req_agendamento_horario",
)

urlpatterns = [
    path("api/", include(router.urls)),
    path("agendar/", views.agendar, name="agendar"),
    re_path(
        r"^agendar/(?P<id>\d+)/$",
        login_required(views.agendar),
        name="editar_agendamento",
    ),
    path("sucesso/", views.sucesso, name="sucesso"),
    path("teste/", views.teste, name="teste"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", login_required(views.dashboard), name="dashboard"),
    path('editar-agendamentos-sem-data/', login_required(views.editar_agendamentos), {'periodo': 0}, name='editar-agendamentos-sem-data'), # type: ignore
    path('editar-agendamentos-futuros/', login_required(views.editar_agendamentos), {'periodo': 1}, name='editar-agendamentos-futuros'), # type: ignore
    path('editar-agendamentos-antigos/', login_required(views.editar_agendamentos), {'periodo': -1}, name='editar-agendamentos-antigos'), # type: ignore
    path('agendamentos-sem-data/', login_required(views.agendamentos_sem_data), name='agendamentos-sem-data'),
]
