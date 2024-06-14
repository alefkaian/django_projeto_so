from django.db import models
from django.db.models import F, Value
import datetime as dt
from django.utils import timezone
from django.db.models.functions import Concat


class Agendamento(models.Model):
    TIPO_DE_ANIMAL_CHOICES = [
        (None, "Selecione"),
        ("Cachorro", "Cachorro"),
        ("Gato", "Gato"),
        ("Pássaro", "Pássaro"),
        ("Hamster", "Hasmster"),
        ("Coelho", "Coelho"),
        ("Outro", "Outro"),
    ]

    TIPO_DE_AGENDAMENTO_CHOICES = [
        (None, "Selecione"),
        ("Consulta", "Consulta"),
        ("Exames", "Exames"),
        ("Vacinação", "Vacinação"),
        ("Cirurgia", "Cirurgia"),
    ]

    HORARIO_CHOICES = [
        (None, "Selecione"),
        (dt.time(hour=14), "14:00"),
        (dt.time(hour=15), "15:00"),
        (dt.time(hour=16), "16:00"),
        (dt.time(hour=17), "17:00"),
    ]

    nome_do_tutor = models.CharField(
        max_length=100,
    )
    data_nascimento = models.CharField(
        max_length=10,
    )
    whatsapp = models.CharField(
        max_length=15,
    )
    email = models.EmailField()
    nome_do_animal = models.CharField(
        max_length=100,
    )
    tipo_de_animal = models.CharField(
        max_length=50,
        choices=TIPO_DE_ANIMAL_CHOICES,
    )
    idade_do_animal = models.CharField(
        max_length=50,
    )
    peso_do_animal = models.CharField(
        max_length=50,
    )
    observacoes = models.TextField(blank=True, default="")
    tipo_de_agendamento = models.CharField(
        max_length=20,
        choices=TIPO_DE_AGENDAMENTO_CHOICES,
        default="Consulta",
    )

    data = models.DateField(null=True, default=None)
    horario = models.TimeField(choices=HORARIO_CHOICES, null=True)
    data_de_criacao = models.DateTimeField()

    def save(self, *args, **kwargs):

        if not self.data_de_criacao:
            self.data_de_criacao = timezone.localtime()

        data_agendamento = self.data
        horario_agendamento = self.horario

        if self.tipo_de_agendamento == "Cirurgia" and data_agendamento:
            # Desmarcar todos os agendamentos com a mesma data
            Agendamento.objects.filter(data=data_agendamento).exclude(
                pk=self.pk
            ).update(
                data=None,
                horario=None,
                observacoes=Concat(F("observacoes"), Value(f" <Desmarcado devido a agendamento de cirurgia na data. Data anterior: {data_agendamento.strftime('%d/%m/%Y')}>"))
            )
        elif (data_agendamento and horario_agendamento):
            # Verificar se já existe algum agendamento com a mesma data e horario
            agendamentos_com_mesma_data_hora = Agendamento.objects.filter(
                data=data_agendamento, horario=horario_agendamento
            ).exclude(pk=self.pk)
            # Atualizar os agendamentos existentes sem chamar save()
            agendamentos_com_mesma_data_hora.update(
                data=None,
                horario=None,
                observacoes=Concat(F("observacoes"), Value(f" <Data anterior: {data_agendamento.strftime('%d/%m/%Y')}. Horário anterior: {horario_agendamento.strftime('%H:%M')}>")))

        # Chamar o método save da classe pai para salvar o novo agendamento ou atualizar o existente
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_do_tutor
