# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Servidor de Senha
Módulo com classe senha.
"""
from pymongo import MongoClient
from hmac import compare_digest as comparador
import crypt
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import socket
class ServidorSenha(object):
    """docstring for ServidorSenha."""
    def __init__(self):
        #ip e porta do banco de dados com senha
        self.client= MongoClient('localhost',27017)
        #banco de dados da aplicação
        self.db=self.client.zeus
        #colecao onde as senhas estão armazenadas
        self.colecao=self.db.senhas
        self.on="online"

    def get_colecao():
        return self.senha_auth

    def login(self,usuario,senha):
        """Valida nome e usuário para login"""
        dados=self.colecao.find_one({"login":usuario})
        if(dados is None):
            print("Usuário não encontrado")
            return False,False
        else:
            senha=crypt.crypt(senha,dados['senha'])
            if(comparador(senha,dados['senha'])):
                print("usuário logado")
                return True,dados['root']
            else:
                #senha ou usuário invalido
                print("erro no login")
                return False,False
            #comparador(dados.senha)

    def novo_usuario(self,usuario,senha,root):
        """Cria e insere um usuário no banco"""
        if("True" in root):
            estado=1
        else:
            estado=""
        dados={"login":usuario,"senha":crypt.crypt(senha),"root":bool(estado)}
        try:
            self.colecao.insert_one(dados)
            #sucesso ao criar um usuário.
            return True
        except Exception as e:
            print("erro ao criar o usuário")
            print(e)
            return False
#porta onde o mesmo está sendo executado
porta=8000
#instancia a classe de senha
#SenhaAuth= ServidorSenha()
#Chama de procedimendo remoto RPC
server= SimpleXMLRPCServer(("localhost",porta))
print("Servidor de senha executando na porta",porta)
ip=socket.gethostbyname(socket.gethostname())
print("Executando com o ip",ip)
#registra a instância do Servidor de senha para RPC
server.register_instance(ServidorSenha())
#deixa o servidor de senha em loop
server.serve_forever()
# #senha.login("magno","4363mg")
# senha.cria_usuario("zeus","4363","1")
# #senha.valida_senha("zeus","4363mg")
