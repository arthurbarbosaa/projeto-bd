# Sistema de Gestão de Consultas

## Descrição do Projeto

O **Sistema de Gestão de Consultas** é uma aplicação web desenvolvida em Python utilizando o framework Flask. O objetivo do sistema é facilitar o gerenciamento de consultas médicas, permitindo que usuários (pacientes e médicos) interajam de forma eficiente. O sistema oferece funcionalidades para registrar, listar, editar e excluir pacientes, médicos e consultas, além de gerenciar usuários com diferentes níveis de acesso.

## Funcionalidades

- **Autenticação de Usuários**: Permite que usuários se registrem e façam login no sistema.
- **Gerenciamento de Pacientes**: Cadastro, edição, listagem e exclusão de pacientes.
- **Gerenciamento de Médicos**: Cadastro, edição, listagem e exclusão de médicos.
- **Gerenciamento de Consultas**: Agendamento, edição, listagem e exclusão de consultas médicas.
- **Gerenciamento de Usuários**: Controle de acesso para usuários administradores, permitindo a criação e exclusão de usuários.

## Tecnologias Utilizadas

- **Flask**: Framework web para desenvolvimento em Python.
- **SQLAlchemy**: ORM (Object-Relational Mapping) para interagir com o banco de dados.
- **Bootstrap**: Framework CSS para estilização e responsividade da interface.
- **Font Awesome**: Biblioteca de ícones para melhorar a interface do usuário.

## Rotas do Sistema de Gestão de Consultas

### Autenticação
- **Login**: `/login` — Página de login do sistema.
- **Registrar**: `/registrar` — Página de registro de novos usuários.
- **Logout**: `/logout` — Rota para realizar o logout do usuário.

### Pacientes
- **Listar Pacientes**: `/pacientes` — Exibe a lista de pacientes cadastrados.
- **Criar Paciente**: `/pacientes/criar` — Formulário para cadastrar um novo paciente.
- **Editar Paciente**: `/pacientes/editar/<int:id>` — Formulário para editar os dados de um paciente específico.
- **Deletar Paciente**: `/pacientes/deletar/<int:id>` — Rota para excluir um paciente do sistema.

### Médicos
- **Listar Médicos**: `/medicos` — Exibe a lista de médicos cadastrados.
- **Criar Médico**: `/medicos/criar` — Formulário para cadastrar um novo médico.
- **Editar Médico**: `/medicos/editar/<int:id>` — Formulário para editar os dados de um médico específico.
- **Deletar Médico**: `/medicos/deletar/<int:id>` — Rota para excluir um médico do sistema.

### Consultas
- **Listar Consultas**: `/consultas` — Exibe a lista de consultas agendadas.
- **Criar Consulta**: `/consultas/criar` — Formulário para agendar uma nova consulta.
- **Editar Consulta**: `/consultas/editar/<int:id>` — Formulário para editar uma consulta agendada.
- **Deletar Consulta**: `/consultas/deletar/<int:id>` — Rota para excluir uma consulta agendada.

### Usuários
- **Listar Usuários**: `/usuarios` — Exibe a lista de usuários registrados no sistema.
- **Criar Usuário**: `/usuarios/criar` — Formulário para cadastrar um novo usuário.
- **Deletar Usuário**: `/usuarios/deletar/<int:id>` — Rota para excluir um usuário do sistema.

## Licença

Este projeto está licenciado sob a **MIT License**. Veja o arquivo LICENSE para mais detalhes.
