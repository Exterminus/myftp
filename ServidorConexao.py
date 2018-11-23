# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Servidor de Conexao
"""
import sys
import socket
import _thread as thread
import getpass
import xmlrpc.client
import pickle
from Usuario import Usuario

class ServidorConexao(object):
    """docstring for ServidorConexao."""
    def __init__(self):
        self.porta=int(sys.argv[1])
        self.ip=""
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.bind((self.ip,self.porta))
        self.tcp.listen(1)
        #chamada RPC para o servidor de senha.
        self.senha_auth=xmlrpc.client.ServerProxy("http://localhost:8000/")
        #chamada RPC para o servidor de arquivos.
        self.arquivos=xmlrpc.client.ServerProxy("http://localhost:8001/")
        self.usuarios_logados=[]

    def envia_resposta(self,conexao,dados):
        """envia uma resposta para o cliente"""
        conexao.sendall(dados)
        conexao.send(b'')
        #conexao.sendall(b'\r\n')

    def rpc_senha(self,usuario,senha):
        """Valida a senha e usuario"""
        print(usuario,senha)
        try:
            retorno,permissao=self.senha_auth.login(usuario,senha)
            if(retorno):
                #devolve a resposta de login sucesso
                user=self.sucess_login(usuario,permissao)
                return True,user
            else:
                return False,False
        except xmlrpc.client.Fault as err:
            print("Ocorreu um erro")
            print("Código de erro %d" % err.faultCode)
            print("Fault string: %s" % err.faultString)

    def sucess_login(self,login,permissao):
        """adiciona um novo usuário na lista de usuários logados"""
        #instancia um novo usuario
        user=Usuario(login,permissao)
        #adiciona na lista de usuarios
        self.usuarios_logados.append(user)
        return user

    def comando_invalido(self,conexao):
        """retorna mensagem de comando invalido"""
        msg="Comando inválido ou faltando parametros."
        self.envia_resposta(conexao,pickle.dumps(msg))

    def logoff(self,login):
        """realiza o logoff"""
        for i in range(0,len(self.usuarios_logados)):
            if(login==self.usuarios_logados[i].getLogin()):
                index=i
        self.usuarios_logados.pop(index)

    def processa_comando(self,conexao,comando,user):
        """processa os comandos"""
        #encerra a conexao com o cliente
        comando=pickle.loads(comando)
        instrucao=comando.split(" ")
        comando=instrucao[0]
        if(len(instrucao)>1):
            parametros=instrucao[1]

        if(comando=="quit"):
            print("Logout")
            instrucao={}
            instrucao['quit']="logout"
            instrucao=pickle.dumps(instrucao)
            print(instrucao)
            conexao.sendall(instrucao)
            #logoff(login)
            conexao.close()
            thread.exit()

        elif(comando=="ls"):
            print("Retornando LS")
            instrucao={}
            #print(user.getHome())
            lista=self.arquivos.ls(user.getHome())
            instrucao['ls']=lista
            print("Instrucao LS",instrucao)
            instrucao=pickle.dumps(instrucao)
            self.envia_resposta(conexao,instrucao)
            #conexao.shutdown(socket.SHUT_WR)
        elif(comando =="cd"):
            #print("Comando cd")
            pasta=instrucao
            print("CMD",comando,"Instrucao",instrucao)
            instrucao={}
            path=user.getHome()+pasta[1]
            print("Caminho",path)
            lista,new_path=self.arquivos.cd(path)
            #atualiza a rota da home..
            if(lista is True):
                user.setHome(new_path)
            print("Retorno cd",lista)
            instrucao['cd']=lista
            instrucao['home']=user.getHome()
            print("Instrucao CD",instrucao)
            instrucao=pickle.dumps(instrucao)
            self.envia_resposta(conexao,instrucao)
            #conexao.shutdown(socket.SHUT_WR)
        elif(comando=="mkdir"):
            #print("mkdir",len(instrucao),comando)
            if(len(instrucao)>1):
                #print(instrucao,parametros)
                #print(user.getHome()+parametros)
                instrucao={}
                #print(user.getHome())
                estado=self.arquivos.mkdir(user.getHome()+"/"+parametros)
                instrucao['mkdir']=estado
                instrucao=pickle.dumps(instrucao)
                self.envia_resposta(conexao,instrucao)
        elif(comando=="delete"):
            #print("mkdir",len(instrucao),comando)
            if(len(instrucao)>1):
                #print(instrucao,parametros)
                #print(user.getHome()+parametros)
                instrucao={}
                #print(user.getHome())
                estado=self.arquivos.delete(user.getHome()+"/"+parametros)
                instrucao['delete']=estado
                instrucao=pickle.dumps(instrucao)
                self.envia_resposta(conexao,instrucao)
        elif(comando=="get"):
                #print("Comando cd")
                pasta=instrucao
                instrucao={}
                path=user.getHome()+pasta[1]
                #print("Caminho",path)
                lista,file=self.arquivos.get(path)
                #atualiza a rota da home..
                if(lista is True):
                    instrucao['get']=True
                    instrucao['file']=file
                    instrucao['nome']=pasta[1]
                else:
                    instrucao['get']=False
                instrucao=pickle.dumps(instrucao)
                self.envia_resposta(conexao,instrucao)

        elif(comando=="rmdir"):
            if(len(instrucao)>1):
                #print(instrucao,parametros)
                #print(user.getHome()+parametros)
                instrucao={}
                #print(user.getHome())
                estado=self.arquivos.rmdir(user.getHome()+"/"+parametros)
                instrucao['rmdir']=estado
                instrucao=pickle.dumps(instrucao)
                self.envia_resposta(conexao,instrucao)
            else:
                self.comando_invalido(conexao)
        else:
            print('sending data back to the client')
            self.envia_resposta(conexao,pickle.dumps(comando))

    def conectado(self,connection, cliente):
        """verificar o disparo e encerramento de threads"""
        msg='Bem vindo ao Zeus FTP v 1.0 2018.'
        msg=pickle.dumps(msg)
        connection.sendall(msg)
        #dicionario do estado de resposta
        estado_login={}
        estado_login['estado']=False
        data=connection.recv(1024)
        dados_login=pickle.loads(data)
        retorno,user =self.rpc_senha(dados_login['usuario'],dados_login['senha'])
        if(retorno):
            estado_login['estado']=True
            estado_login['home']=user.getHome()
            #sucesso ao realizar o login
            connection.sendall(pickle.dumps(estado_login))
        else:
            #erro ao efetuar o login
            connection.sendall(pickle.dumps(estado_login))
        if(estado_login['estado']== True):
            while True:
                # Wait for a connection
                try:
                    print('connection from', cliente)
                    # Receive the data in small chunks and retransmit it
                    data = connection.recv(1024)
                    print(data)
                    print('received',pickle.loads(data))
                    self.processa_comando(connection,data,user)
                    # if data:
                    #     print('sending data back to the client')
                    #     connection.sendall(data)
                    # else:
                    #     print('no data from', cliente)
                    #     break
                except Exception as e:
                    # Clean up the connection
                    print("e",e)
                    connection.close()
                    thread.exit()

    def iniciar_servidor(self):
        print("Servidor Iniciado.. na porta",self.porta)
        while True:
            con, cliente = self.tcp.accept()
            thread.start_new_thread(self.conectado, tuple([con, cliente]))


servidor= ServidorConexao()
servidor.iniciar_servidor()
