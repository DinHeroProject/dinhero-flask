# DinHero Flask

DinHero Flask é uma API desenvolvida em Python utilizando o framework Flask, destinada à gestão de cursos, mentorias e usuários. O projeto é modularizado em camadas para facilitar manutenção, escalabilidade e testes.

## Sumário
- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Endpoints Principais](#endpoints-principais)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Visão Geral
Este projeto tem como objetivo fornecer uma API RESTful para gerenciamento de cursos, mentorias e usuários, com persistência em banco de dados SQLite.

## Funcionalidades
- Cadastro, consulta, atualização e remoção de usuários
- Gerenciamento de cursos
- Gerenciamento de mentorias
- Estrutura modular (models, dao, services, routes)
- Tratamento de erros

## Estrutura do Projeto
```
app.py                # Arquivo principal para inicialização da aplicação
app/
  ├── dao/            # Data Access Object (acesso ao banco de dados)
  ├── database/       # Configuração e arquivo do banco de dados
  ├── models/         # Modelos das entidades (User, Course, Mentorship)
  ├── routes/         # Rotas da API Flask
  ├── services/       # Lógica de negócio
  └── utils/          # Utilitários e tratamento de erros
```

## Instalação
1. Clone o repositório:
	```bash
	git clone https://github.com/DinHeroProject/dinhero-flask.git
	cd dinhero-flask
	```
2. Crie e ative um ambiente virtual:
	```bash
	python -m venv .venv
	source .venv/Scripts/activate  # Windows
	# ou
	source .venv/bin/activate      # Linux/Mac
	```
3. Instale as dependências:
	```bash
	pip install -r requirements.txt
	```

## Como Executar
1. Execute a aplicação Flask:
	```bash
	python app.py
	```
2. Acesse a API em `http://localhost:5000`

## Endpoints Principais
- `/users` - CRUD de usuários
- `/courses` - CRUD de cursos
- `/mentorships` - CRUD de mentorias

Consulte os arquivos em `app/routes/` para detalhes de cada endpoint.

## Contribuição
Pull requests são bem-vindos! Para grandes mudanças, abra uma issue primeiro para discutir o que deseja modificar.

## Licença
Este projeto está sob a licença MIT.