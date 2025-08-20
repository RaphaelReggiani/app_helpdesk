# App HELPDESK

Desenvolvida com **Python**, **Django** e **Django REST Framework** (Inclui API com autenticação via token para acesso seguro aos dados), utilizando **HTML** e **CSS**. 

A aplicação configura-se como um site de suporte ao cliente, utilizando tickets para comunicação entre membros da Staff e os Clientes.

OBS: O foco deste aplicativo é o uso direto das funções nativas do Django (utilizando por exemplo: User, UserManager, etc).

## Funcionalidades

- Cadastramento de usuários tipo cliente no site;
- Cadastramento de usuário tipo suporte, permitido apenas por membros da staff;
- Seção de cadastro e login de usuários (incluindo todas as validações nativas do Django);
- O acesso às funcionalidade do site (abertura de tickets / comunicação com a equipe de suporte), só ocorre com usuário logado;
- Os clientes possuem acesso apenas aos seus tickets, podendo enviar mensagens após a abertura dos mesmos, para algum complemento ou atualrizar informações para os membros da Staff;
- Os membros da Staff (Suporte), tem acesso geral ao site, incluindo todos os tickets abertos no site e permissão para criar usuários da equipe de Suporte;
- Funcionalidade de: Esqueceu a senha?, realizada através de envio de um e-mail para a redefinição de senha, com token de autenticação.

## Imagens da Aplicação

### Página Inicial - Sem login
![Home Page](readme_assets/home_sem_login.png)

### Página Inicial - Usuário Cliente logado
![Home Page - Cliente](readme_assets/home_login_cliente.png)

### Página Inicial - Usuário Suporte logado
![Home Page - Staff](readme_assets/home_login_staff.png)

### Cadastro de Usuários / Log in
![Cadastro / Log in](readme_assets/cadastro_login_page.png)

### Cadastro de Usuários - Staff
![Cadastro - Staff](readme_assets/cadastro_staff.png)

### Informações do Usuário - Cliente
![Informações de usuário - Cliente](readme_assets/perfil_update_cliente.png)

### Página de Esqueceu a senha? - Parte 1
![Redefinição de senha - Parte 1](readme_assets/redefinir_senha.png)

### Página de Esqueceu a senha? - Parte 2
![Redefinição de senha - Parte 2](readme_assets/redefinir_senha_email_sent.png)

### Página de Esqueceu a senha? - Parte 3
![Redefinição de senha - Parte 3](readme_assets/definir_nova_senha.png)

### Página de Esqueceu a senha? - Parte 4
![Redefinição de senha - Parte 4](readme_assets/senha_redefinida.png)

### Registrar Ticket  
![Registro de ticket](readme_assets/ticket_create.png)

### Detalhes do Ticket - Cliente  
![Detalhes do Ticket - Cliente](readme_assets/cliente_ticket_detail.png)

### Detalhes do Ticket - Staff  
![Detalhes do Ticket - Staff](readme_assets/staff_ticket_detail.png)

### Lista de Tickets - Cliente  
![Lista de Tickets - Cliente](readme_assets/cliente_ticket_list.png)

### Lista de Tickets - Staff  
![Lista de Tickets - Staff](readme_assets/tickets_list_staff.png)