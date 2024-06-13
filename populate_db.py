import os
import django
from datetime import datetime, timedelta
import random
import string

# Configure o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetoSO.settings')
django.setup()

# Agora você pode importar o modelo Agendamento
from agendamento.models import Agendamento

def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date

def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def random_weekday(start_date, end_date):
    weekdays = [1, 2, 3, 4, 5]  # Segunda a sexta-feira
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    while random_date.weekday() not in weekdays:
        random_date += timedelta(days=1)
    return random_date

# Datas entre 2 meses atrás e 2 meses à frente
data_atual = datetime.now()
data_inicio = data_atual - timedelta(days=60)
data_fim = data_atual + timedelta(days=60)

nomes_tutor = ["Maria", "João", "Pedro", "Ana", "Mariana", "José"]
tipos_animal = ["Cachorro", "Gato", "Pássaro", "Hamster", "Coelho", "Outro"]
tipos_agendamento = ["Consulta", "Exames", "Vacinação", "Cirurgia"]

# Popule o banco de dados com agendamentos
for _ in range(100):
    data_agendamento = random_weekday(data_inicio, data_fim).strftime("%Y-%m-%d")
    horario_agendamento = random.choice([datetime.strptime("14:00:00", "%H:%M:%S").time(), datetime.strptime("15:00:00", "%H:%M:%S").time(), datetime.strptime("16:00:00", "%H:%M:%S").time(), datetime.strptime("17:00:00", "%H:%M:%S").time()]).strftime("%H:%M:%S")
    tipo_de_agendamento = random.choice(tipos_agendamento)

    # Verificar se já existe um agendamento para este horário nesta data
    if Agendamento.objects.filter(data=data_agendamento, horario=horario_agendamento).exists():
        continue

    if Agendamento.objects.filter(data=data_agendamento, tipo_de_agendamento="Cirurgia").exists():
        continue

    nome_do_tutor = random.choice(nomes_tutor)
    data_nascimento = random_date(datetime(1950, 1, 1), datetime(2010, 1, 1)).strftime("%Y-%m-%d")
    whatsapp = '(' + str(random.randint(11, 99)) + ') ' + str(random.randint(10000, 99999)) + '-' + str(random.randint(1000, 9999))
    email = f"{nome_do_tutor.lower()}@example.com"
    nome_do_animal = random_string(6)
    tipo_de_animal = random.choice(tipos_animal)
    idade_do_animal = random.randint(1, 20)
    peso_do_animal = random.randint(1, 50)
    observacoes = random_string(20)

    agendamento = Agendamento(nome_do_tutor=nome_do_tutor, data_nascimento=data_nascimento, whatsapp=whatsapp
                               , email=email, nome_do_animal=nome_do_animal, tipo_de_animal=tipo_de_animal
                               , idade_do_animal=idade_do_animal, peso_do_animal=peso_do_animal
                               , observacoes=observacoes, tipo_de_agendamento=tipo_de_agendamento
                               , data=data_agendamento, horario=horario_agendamento)
    agendamento.save()

    # Crie o objeto Agend
