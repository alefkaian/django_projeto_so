# Generated by Django 5.0.6 on 2024-06-07 13:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamento', '0003_alter_agendamento_observacoes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendamento',
            name='horario',
            field=models.TimeField(blank=True, choices=[(None, 'Selecione'), (datetime.time(14, 0), '14:00'), (datetime.time(15, 0), '15:00'), (datetime.time(16, 0), '16:00'), (datetime.time(17, 0), '17:00')], null=True),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='tipo_de_agendamento',
            field=models.CharField(choices=[('None', 'Selecione'), ('Consulta', 'Consulta'), ('Exames', 'Exames'), ('Vacinação', 'Vacinação'), ('Cirurgia', 'Cirurgia')], default='Consulta', max_length=20),
        ),
        migrations.AlterField(
            model_name='agendamento',
            name='tipo_de_animal',
            field=models.CharField(choices=[('None', 'Selecione'), ('Cachorro', 'Cachorro'), ('Gato', 'Gato'), ('Pássaro', 'Pássaro'), ('Hamster', 'Hasmster'), ('Coelho', 'Coelho'), ('Outro', 'Outro')], max_length=50),
        ),
    ]
