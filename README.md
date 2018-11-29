# Myftp - ZeusFTP v 1.0
Cliente FTP distríbuido.
ZeusFTP é um cliente e servidor ftp distríbuido implementado para a disciplina de sistemas distríbuidos. O mesmo utiliza conexão segura com SSL e chamada de procedimento remoto para permitir a comunição entre os servidores.

***Carlos Magno***
***UFSJ 2018***

## Arquitetura do projeto
O projeto esta organizado da seguinte maneira:
* cliente - Permite a interação do usuário com servidor de conexão. A conexão entre o cliente e o servidor é realizada através do protocolo TCP.
* Servidor de conexão - Comunica com servidor de arquivos e senhas utilizando RCP.
* Servidor de arquivos - Armazena as funções validas, manipula os arquivos.
* Servidor de Senha - Realiza a comunicação com o banco de dados.

## O que configurar?

* Configure o ip do servidor de senha e de arquivos no servidor de conexão.

* Execute o criar_usuario.py antes de iniciar o servidor de senha.
* O usuário padrão criado possui a senha 1234 e login zeus.
## Como Executar
Como executar:
1. Inicie o servidor de senha.
>python3 ServidorSenha.py
2. Inicie o Servidor de Arquivos
>python3 ServidorArquivo.py
3.  Inicie o servidor de Conexao, verifique os ip’s do servidor de arquivos e senha
antes de executar.
>python3 ServidorConexao.py [porta]
4.  Inicie o cliente:
>python3 Cliente.py [ip
servidor
conexao] [porta] [login]

## Requisitos
- python3
- mondodb
- pymongo

## Desenvolvedor
![](https://github.com/Exterminus.png?size=100)
Carlos Magno ([github](https://github.com/Exterminus))
