# Aplicação de agendamentos para uma Clínica Veterinária

Este projeto foi feito para uma disciplina de extensão em colaboração com o curso de Medicina Veterinária e tem como objetivo criar uma aplicação de agendamento para a Clínica Veterinária do curso. Os clientes só possuem acesso à página de agendamento e podem fazer o agendamento por si mesmos enquanto o administrador pode fazer agendamentos (cirurgia é agendada apenas por ele), modificar agendamentos existentes (como realocar datas) e verificar a agenda semanal, além de também poder visualizar todos os agendamentos em forma de tabela.


## Funcionalidades

* Cadastrar agendamentos

![]() ![]()

* Editar agendamentos

![]() ![]()

* Visualizar agenda semanal

![]() ![]()

* Visualizar tabela de agendamentos com função de busca

![]() ![]()

* Login de administrador

![]() ![]()

* Regras de negócio específicas da clínica (ex: Segunda e Terça-feira podem ser dias exclusivos para cirurgia se houver, todos os outros agendamentos devem ser desmarcados caso haja)
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
python -m venv app_env
.\app_env\Scripts\activate
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
python3 -m venv app_env
source app_env/bin/activate
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