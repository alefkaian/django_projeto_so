import random
from datetime import datetime, timedelta
from django.utils import timezone
from agendamento.models import Agendamento

def random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

start_date = timezone.now() - timedelta(days=60)  # 2 meses atrás
end_date = timezone.now() + timedelta(days=60)    # 2 meses no futuro

for _ in range(100):  # Quantidade de registros a serem criados
    data = random_date(start_date, end_date)
    if data.weekday() < 5:  # Verifica se é um dia de semana (0 a 4 para segunda a sexta-feira)
        agendamento = Agendamento(
            nome_do_tutor="Nome do Tutor",
            data_nascimento="01/01/1990",
            whatsapp="999999999",
            email="email@example.com",
            nome_do_animal="Nome do Animal",
            tipo_de_animal=random.choice([choice[0] for choice in Agendamento.TIPO_DE_ANIMAL_CHOICES[1:]]),  # Exclui o primeiro item ("Selecione")
            idade_do_animal="2 anos",
            peso_do_animal="10 kg",
            observacoes="Observações",
            tipo_de_agendamento=random.choice([choice[0] for choice in Agendamento.TIPO_DE_AGENDAMENTO_CHOICES[1:]]),  # Exclui o primeiro item ("Selecione")
            data=data,
            horario=random.choice([choice[0] for choice in Agendamento.HORARIO_CHOICES[1:]]),  # Exclui o primeiro item ("Selecione")
        )
        agendamento.save()