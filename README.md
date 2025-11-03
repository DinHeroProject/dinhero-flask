# DinHero Flask

DinHero Flask é uma API desenvolvida em Python utilizando o framework Flask, destinada à gestão de cursos, mentorias e usuários. O projeto é modularizado em camadas para facilitar manutenção, escalabilidade e testes.

## Sumário
- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Endpoints Principais](#endpoints-principais)
- [Sistema de Perfil de Usuário](#sistema-de-perfil-de-usuário)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Visão Geral
Este projeto tem como objetivo fornecer uma API RESTful para gerenciamento de cursos, mentorias e usuários, com persistência em banco de dados SQLite.

## Funcionalidades
- Cadastro, consulta, atualização e remoção de usuários
- **Sistema completo de perfil de usuário com preferências de aprendizagem**
- Gerenciamento de cursos
- Gerenciamento de mentorias
- Autenticação JWT
- Estrutura modular (models, dao, services, routes)
- Tratamento de erros e validações
- Sistema de perfil personalizado

## Estrutura do Projeto
```
app.py                # Arquivo principal para inicialização da aplicação
app/
  ├── dao/            # Data Access Object (acesso ao banco de dados)
  │   ├── user_dao.py
  │   ├── profile_dao.py      # DAO para perfis de usuário
  │   ├── course_dao.py
  │   └── mentorship_dao.py
  ├── database/       # Configuração e arquivo do banco de dados
  ├── models/         # Modelos das entidades (User, Course, Mentorship)
  ├── routes/         # Rotas da API Flask
  ├── services/       # Lógica de negócio
  └── utils/          # Utilitários e tratamento de erros
migrations/           # Scripts de migração do banco
PROFILE_API_DOCS.md   # Documentação detalhada da API de perfil
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
2. Acesse a API em `http://localhost:3333`

## Endpoints Principais
- `/users` - CRUD de usuários
- `/users/<user_id>/profile` - GET/PUT para gerenciar perfis de usuário
- `/courses` - CRUD de cursos
- `/mentorships` - CRUD de mentorias
- `/login` - Autenticação de usuários

Consulte os arquivos em `app/routes/` para detalhes de cada endpoint.

## Sistema de Perfil de Usuário

O sistema de perfil permite que usuários personalizem suas informações e preferências de aprendizagem.

### Campos do Perfil
- **avatar_url**: URL da imagem de perfil
- **bio**: Biografia do usuário (máx. 500 caracteres)
- **date_of_birth**: Data de nascimento
- **gender**: Gênero (masculino, feminino, outro, prefiro_nao_informar)
- **country**: País do usuário
- **language_preference**: Idioma preferido (pt-br, en, es, etc.)
- **learning_style_preference**: Estilo de aprendizagem (visual, auditivo, cinestésico, leitura_escrita)
- **content_complexity_preference**: Complexidade de conteúdo (básico, intermediário, avançado)
- **video_length_preference**: Duração de vídeos preferida (curto, médio, longo)

### Exemplo de Uso

**Obter perfil:**
```bash
GET /users/1/profile
Authorization: Bearer {token}
```

**Atualizar perfil:**
```bash
PUT /users/1/profile
Authorization: Bearer {token}
Content-Type: application/json

{
  "bio": "Entusiasta de educação financeira",
  "language_preference": "pt-br",
  "learning_style_preference": "visual",
  "content_complexity_preference": "intermediario"
}
```

Para documentação completa da API de perfil, consulte [PROFILE_API_DOCS.md](PROFILE_API_DOCS.md).

### Testes

Execute o script de testes para validar a API de perfil:
```bash
python test_profile_api.py
```

## Contribuição
Pull requests são bem-vindos! Para grandes mudanças, abra uma issue primeiro para discutir o que deseja modificar.

## Licença
Este projeto está sob a licença MIT.







