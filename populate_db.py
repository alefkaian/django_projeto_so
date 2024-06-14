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
    weekdays = [0, 1, 2, 3, 4]  # Segunda a sexta-feira
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

nomes_tutor = ["Maria", "Joao", "Pedro", "Ana", "Mariana", "Jose"]
sobrenomes_tutor = ["Silva", "da Silva", "Melo", "Almeida", "Pereira", "Santos", "de Souza", "da Costa", "Barbosa", "Rocha", "Lima"]
nomes_pet = ["Rex", "Toto", "Rengar", "Lala", "Mimi", "Caramelo", "Nemo", "Nala", "Pipoca", "Pudim", "Mel", "Bolinha"]
tipos_animal = ["Cachorro", "Gato", "Pássaro", "Hamster", "Coelho", "Outro"]
tipos_agendamento = ["Consulta", "Exames", "Vacinação", "Cirurgia"]

# Popule o banco de dados com agendamentos
for _ in range(100):
    data_random = random_weekday(data_inicio, data_fim)
    data_agendamento = data_random
    horario_agendamento = random.choice([datetime.strptime("14:00:00", "%H:%M:%S").time(), datetime.strptime("15:00:00", "%H:%M:%S").time(), datetime.strptime("16:00:00", "%H:%M:%S").time(), datetime.strptime("17:00:00", "%H:%M:%S").time()])
    tipo_de_agendamento = random.choice(tipos_agendamento)

    # Verificar se já existe um agendamento para este horário nesta data
    if Agendamento.objects.filter(data=data_agendamento, horario=horario_agendamento).exists():
        continue

    if Agendamento.objects.filter(data=data_agendamento, tipo_de_agendamento="Cirurgia").exists():
        continue

    if tipo_de_agendamento == "Cirurgia" and data_random.weekday() != 0 and data_random.weekday() != 1:
        continue

    nome_do_tutor = random.choice(nomes_tutor) + " " + random.choice(sobrenomes_tutor)
    data_nascimento = random_date(datetime(1950, 1, 1), datetime(2010, 1, 1)).strftime("%d/%m/%Y")
    whatsapp = '(' + str(random.randint(11, 99)) + ') ' + str(random.randint(10000, 99999)) + '-' + str(random.randint(1000, 9999))
    email = f"{nome_do_tutor.lower().replace(' ', '.')}@example.com"
    nome_do_animal = random.choice(nomes_pet)
    tipo_de_animal = random.choice(tipos_animal)
    idade_do_animal = str(random.randint(1, 20)) + random.choice([" anos", " meses", " dias"])
    peso_do_animal = str(random.randint(1, 50)) + random.choice([" kg", " g"])
    observacoes = random_string(20)

    agendamento = Agendamento(nome_do_tutor=nome_do_tutor, data_nascimento=data_nascimento, whatsapp=whatsapp
                               , email=email, nome_do_animal=nome_do_animal, tipo_de_animal=tipo_de_animal
                               , idade_do_animal=idade_do_animal, peso_do_animal=peso_do_animal
                               , observacoes=observacoes, tipo_de_agendamento=tipo_de_agendamento
                               , data=data_agendamento, horario=horario_agendamento)
    agendamento.save()

    # Crie o objeto Agend
