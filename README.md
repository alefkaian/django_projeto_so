# Aplicação de agendamentos para uma Clínica Veterinária

Este projeto foi feito para uma disciplina de extensão em colaboração com o curso de Medicina Veterinária e tem como objetivo criar uma aplicação de agendamento para a Clínica Veterinária do curso. Os clientes só possuem acesso à página de agendamento e podem fazer o agendamento por si mesmos enquanto o administrador pode fazer agendamentos (cirurgia é agendada apenas por ele), modificar agendamentos existentes (como realocar datas), verificar a agenda semanal, além de também poder visualizar todos os agendamentos em forma de tabela.


## Funcionalidades

* Cadastrar agendamentos

<img width=auto height=360px alt="Página de agendamento mobile" src="https://github.com/user-attachments/assets/8e7aac45-10ff-4543-8e4c-c8e11c1bbec4" />
<img width=100% height=auto alt="Image" src="https://github.com/user-attachments/assets/f20bdb5d-dda6-48ca-9eb5-d0b14f492e82" />
<br>
<br>

* Editar agendamentos

<img width=100% height=auto alt="Editar agendamento desktop" src="https://github.com/user-attachments/assets/e53693f4-dc82-47b6-a1e2-cb7d4b8095b2" />
<br>
<br>

* Visualizar agenda semanal

<img width=100% height=auto alt="Dashboard desktop" src="https://github.com/user-attachments/assets/44c18f62-93ee-4c53-9e38-df277b1960ab" />
<br>
<br>

* Visualizar tabela de agendamentos com função de busca

<img width=100% height=auto alt="Tabela desktop" src="https://github.com/user-attachments/assets/c5e772e5-b26f-4553-a438-93c46a636233" />
<br>
<br>

* Login de administrador
* Regras de negócio específicas da clínica (ex: Segunda e Terça-feira são dias exclusivos para cirurgia se houver alguma e, caso haja, todos os outros agendamentos do dia devem ser desmarcados)
* Design responsivo
* Validação de formulário
* Proteção contra ataques CSRF
* Dashboard do Django Admin


## Tecnologias utilizadas

Este projeto foi desenvolvido utilizando as seguintes tecnologias:

* **Banco de Dados:** Sqlite
* **Backend:** Django 5.1
* **Front-end:** Django Template Language, Bootstrap 5.3.3, JavaScript, JQuery 3.7.1

## Configuração e Execução Local

### Pré-requisitos

* Python > 3.11

### Rodando no Windows

1. **Clone o repositório e acesse a pasta raíz do projeto:**

```bash
git clone https://github.com/alefkaian/django_projeto_so.git
cd django_projeto_so
```

2. **Crie um ambiente virtual e o ative para a instalação das dependências:**

```bash
python -m venv django_env
.\django_env\Scripts\activate
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Faça as migrações do banco:**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crie a conta de administrador para testes:**

```bash
python manage.py createsuperuser
```
\*\*Siga as intruções no terminal para criar o nome de usuário e senha de admin

6. **Execute a aplicação:**
   
```bash
python manage.py runserver
```

A aplicação será iniciada e estará rodando em `http://localhost:8000`

7. **(Opcional) Popule o banco para visualizar alguns agendamentos:**

```bash
python populate_db.py
```

### Rodando no Linux

1. **Clone o repositório e acesse a pasta raíz do projeto:**

```bash
git clone https://github.com/alefkaian/django_projeto_so.git
cd django_projeto_so
```

2. **Crie um ambiente virtual e o ative para a instalação das dependências:**

```bash
python3 -m venv django_env
source django_env/bin/activate
```

3. **Instale as dependências:**

```bash
pip3 install -r requirements.txt
```

4. **Faça as migrações do banco:**

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

5. **Crie a conta de administrador para testes:**

```bash
python3 manage.py createsuperuser
```
\*\*Siga as intruções no terminal para criar o nome de usuário e senha de admin

6. **Execute a aplicação:**
   
```bash
python3 manage.py runserver
```

A aplicação será iniciada e estará rodando em `http://localhost:8000`

7. **(Opcional) Popule o banco para visualizar alguns agendamentos:**

```bash
python3 populate_db.py
```

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [License](LICENSE) para mais detalhes
