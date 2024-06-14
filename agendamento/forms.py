from django import forms
from .models import Agendamento
import datetime as dt
from re import search


class AgendamentoForm(forms.ModelForm):

    data = forms.DateField(required=True)  # type: ignore
    horario = forms.ChoiceField(required=True, choices=Agendamento.HORARIO_CHOICES)
    tipo_de_animal = forms.ChoiceField(
        required=True, choices=Agendamento.TIPO_DE_ANIMAL_CHOICES
    )

    class Meta:
        model = Agendamento
        fields = [
            "nome_do_tutor",
            "data_nascimento",
            "whatsapp",
            "email",
            "nome_do_animal",
            "tipo_de_animal",
            "idade_do_animal",
            "peso_do_animal",
            "observacoes",
            "data",
            "horario",
        ]
        labels = {
            "nome_do_tutor": "Nome do tutor",
            "data_nascimento": "Data de nascimento",
            "whatsapp": "Telefone (whatsapp)",
            "email": "Endereço de e-mail",
            "nome_do_animal": "Nome do Animal",
            "tipo_de_animal": "Tipo de Animal",
            "idade_do_animal": "Idade do Animal",
            "peso_do_animal": "Peso do Animal",
            "observacoes": "Observações",
            "data": "Data da Consulta",
            "horario": "Horário da Consulta",
        }
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"placeholder": "dd/mm/aaaa"}),
            "whatsapp": forms.TextInput(
                attrs={
                    "maxlength": "15",
                    "placeholder": "(99) 99999-9999",
                }
            ),
            "idade_do_animal": forms.TextInput(
                attrs={"placeholder": "ex: 3 anos, 6 meses"}
            ),
            "peso_do_animal": forms.TextInput(attrs={"placeholder": "ex: 15 kg, 500g"}),
            "observacoes": forms.Textarea(
                attrs={
                    "placeholder": "Raça do animal, temperamento, cuidados especiais e outras informações que julgar importantes.",
                    "maxlength": "180",
                }
            ),
        }

    def clean_observacoes(self):
        observacoes = self.cleaned_data["observacoes"]
        if len(observacoes) > 180:
            raise forms.ValidationError("Limite de 180 caracteres")
        return observacoes

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data["data_nascimento"]
        if len(data_nascimento) != 10:
            raise forms.ValidationError("Data de nascimento inválida")
        return data_nascimento

    def clean_whatsapp(self):
        whatsapp = self.cleaned_data["whatsapp"]
        if len(whatsapp) != 15:
            raise forms.ValidationError("Número de telefone inválido")
        return whatsapp

    def clean_idade_do_animal(self):
        idade_do_animal = self.cleaned_data["idade_do_animal"]
        if not search(r"\d", idade_do_animal) or not search(
            r"[a-zA-Z]", idade_do_animal
        ):
            raise forms.ValidationError("Idade inválida")
        return idade_do_animal

    def clean_peso_do_animal(self):
        peso_do_animal = self.cleaned_data["peso_do_animal"]
        if not search(r"\d", peso_do_animal) or not search(r"[a-zA-Z]", peso_do_animal):
            raise forms.ValidationError("Peso inválido")
        return peso_do_animal

    def clean(self):
        data = self.cleaned_data.get("data")
        horario = self.cleaned_data.get("horario")

        if data and horario:
            if Agendamento.objects.filter(data=data, horario=horario).exists():
                raise forms.ValidationError("Horário indisponível")

        return self.cleaned_data


class AgendamentoFormAdm(forms.ModelForm):

    nome_do_tutor = forms.CharField(label="Nome do tutor")
    data_nascimento = forms.CharField(
        label="Data de nascimento",
        required=False,
        widget=forms.DateInput(attrs={"placeholder": "dd/mm/aaaa"}),
    )
    whatsapp = forms.CharField(
        label="Whatsapp",
        required=False,
        widget=forms.TextInput(
            attrs={
                "maxlength": "15",
                "placeholder": "(99) 99999-9999",
            }
        ),
    )
    email = forms.EmailField(label="E-mail", required=False)
    nome_do_animal = forms.CharField(label="Nome do Animal", required=False)
    tipo_de_animal = forms.ChoiceField(
        label="Tipo de Animal",
        required=False,
        choices=Agendamento.TIPO_DE_ANIMAL_CHOICES,
    )
    idade_do_animal = forms.CharField(
        label="Idade do Animal",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "ex: 3 anos, 6 meses"}),
    )
    peso_do_animal = forms.CharField(
        label="Peso do Animal",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "ex: 15 kg, 500g"}),
    )
    observacoes = forms.CharField(
        label="Observações",
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Raça do animal, temperamento, cuidados especiais e outras informações que julgar importantes.",
                "maxlength": "180",
            }
        ),
    )
    tipo_de_agendamento = forms.ChoiceField(
        label="Tipo de Agendamento",
        required=False,
        choices=Agendamento.TIPO_DE_AGENDAMENTO_CHOICES,
    )
    data = forms.DateField(label="Data do Agendamento", required=False)  # type: ignore
    horario = forms.ChoiceField(
        label="Horário do Agendamento",
        required=False,
        choices=Agendamento.HORARIO_CHOICES,
    )

    class Meta:
        model = Agendamento

        fields = [
            "nome_do_tutor",
            "data_nascimento",
            "whatsapp",
            "email",
            "nome_do_animal",
            "tipo_de_animal",
            "idade_do_animal",
            "peso_do_animal",
            "observacoes",
            "tipo_de_agendamento",
            "data",
            "horario",
        ]
        labels = {
            "nome_do_tutor": "Nome do tutor",
            "data_nascimento": "Data de nascimento",
            "whatsapp": "Telefone (whatsapp)",
            "email": "Endereço de e-mail",
            "nome_do_animal": "Nome do Animal",
            "tipo_de_animal": "Tipo de Animal",
            "idade_do_animal": "Idade do Animal",
            "peso_do_animal": "Peso do Animal",
            "observacoes": "Observações",
            "tipo_de_agendamento": "Tipo de Agendamento",
            "data": "Data do Agendamento",
            "horario": "Horário do Agendamento",
        }

    def clean_data(self):
        data_clean = self.cleaned_data.get("data")
        if not data_clean:
            return None
        return data_clean

    def clean_horario(self):
        horario_clean = self.cleaned_data.get("horario")
        if not horario_clean:
            return None
        return horario_clean

    def clean(self):
        cleaned_data = super().clean()
        data_clean = self.cleaned_data.get("data")
        if Agendamento.objects.exclude(id=self.instance.id).filter(
            data=data_clean, tipo_de_agendamento="Cirurgia"
        ).exists():
            raise forms.ValidationError(
                "Horário indisponível. Desmarque a cirurgia primeiro!"
            )

        return cleaned_data
