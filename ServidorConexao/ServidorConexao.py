# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Servidor de Conexao
Carlos Magno
UFSJ
"""
import sys
import socket
import _thread as thread
import getpass
import xmlrpc.client
import pickle
from Usuario import Usuario
import ssl
import socket
class ServidorConexao(object):
    """docstring for ServidorConexao."""
    def __init__(self):
        self.porta=int(sys.argv[1])
        self.ip=""
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        #carrega a chave do servidor..
        self.context.load_cert_chain(certfile="chave_servidor/server.pem", keyfile="chave_servidor/server.key")
        self.tcp.bind((self.ip,self.porta))
        self.tcp.listen(1)
        #chamada RPC para o servidor de senha.
        # Atualizar ip servidor de senha.
        self.senha_auth=xmlrpc.client.ServerProxy("http://localhost:8000/")
        #chamada RPC para o servidor de arquivos.
        # Atualalizr ip do servidor de arquivos.
        self.arquivos=xmlrpc.client.ServerProxy("http://localhost:8001/")
        self.usuarios_logados=[]

    def envia_resposta(self,conexao,dados):
        """envia uma resposta para o cliente"""
        conexao.sendall(dados)

    def rpc_senha(self,usuario,senha):
        """Valida a senha e usuario"""
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

        if(comando['cmd']=="quit"):
            print("Logout")
            instrucao={}
            instrucao['quit']="logout"
            instrucao=pickle.dumps(instrucao)
            print(instrucao)
            conexao.sendall(instrucao)
            #logoff(login)
            conexao.close()
            thread.exit()
        elif(comando['cmd']=="newuser"):

            instrucao={}
            if(comando['user'] and user.getPermissao()):
                usuario=comando['user']
                senha=comando['senha']
                permissao=comando['permissao']
                estado=self.senha_auth.novo_usuario(usuario,senha,permissao)
                if(estado):
                    #cria uma nova home de Usuario
                    estado=self.arquivos.novahome(usuario)
                instrucao['newuser']=estado
                instrucao['root']=user.getPermissao()

                instrucao=pickle.dumps(instrucao)
                self.envia_resposta(conexao,instrucao)
            else:
                instrucao['newuser']=False
                instrucao['root']=user.getPermissao()
                instrucao=pickle.dumps(instrucao)
                self.envia_resposta(conexao,instrucao)
        elif(comando['cmd']=="ls"):
            print("Retornando LS")
            instrucao={}

            lista=self.arquivos.ls(user.getHome())
            instrucao['ls']=lista

            instrucao=pickle.dumps(instrucao)
            self.envia_resposta(conexao,instrucao)

        elif(comando['cmd'] =="cd"):
            #print("Comando cd")
            pasta=comando['caminho']
            print("CMD",comando,"Instrucao",comando['caminho'])
            instrucao={}
            path=user.getHome()+pasta
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

        elif(comando['cmd']=="mkdir"):

            if(comando['caminho']):
                instrucao={}

                estado=self.arquivos.mkdir(user.getHome()+"/"+comando['caminho'])
                instrucao['mkdir']=estado
                instrucao=pickle.dumps(instrucao)
                self.envia_resposta(conexao,instrucao)
        elif(comando['cmd']=="delete"):

            if(comando['caminho']):
                instrucao={}
                #print(user.getHome())
                estado=self.arquivos.delete(user.getHome()+"/"+comando['caminho'])
                instrucao['delete']=estado
                instrucao=pickle.dumps(instrucao)
                self.envia_resposta(conexao,instrucao)
        elif(comando['cmd']=="get"):
                #print("Comando cd")
                print("Comando Get")
                pasta=comando['caminho']
                instrucao={}
                path=user.getHome()+pasta
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

        elif(comando['cmd']=="put"):

                print("Comando put")
                if(comando['file']):
                    nome_arquivo=comando['caminho']
                    instrucao={}
                    path=user.getHome()+nome_arquivo

                    lista,file=self.arquivos.put(path,comando['file'])
                    #atualiza a rota da home..
                    if(lista is True):
                        instrucao['put']=True
                    else:
                        instrucao['put']=False
                    instrucao=pickle.dumps(instrucao)
                    self.envia_resposta(conexao,instrucao)
                else:
                    self.comando_invalido(conexao)


        elif(comando['cmd']=="rmdir"):
            if(comando['caminho']):
                instrucao={}

                estado=self.arquivos.rmdir(user.getHome()+"/"+comando['caminho'])
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
        msg='Bem vindo ao Zeus FTP v 1.0\nConexão segura estabelecida!'
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
                    rec=[]
                    recebido=0
                    data=""
                    while True:
                        data=""
                        #buffer de recebimento dos dados.
                        data=connection.recv(1024)
                        rec.append(data)
                        recebido=len(data)-1024
                        if(recebido<0):
                            break
                    #combina os dados
                    data=pickle.loads(b"".join(rec))
                    self.processa_comando(connection,data,user)

                except Exception as e:
                    # Clean up the connection
                    print("e",e)
                    connection.close()
                    thread.exit()

    def iniciar_servidor(self):
        ip=socket.gethostbyname(socket.gethostname())
        print("Servidor Iniciado.. no IP ",ip," Porta:",self.porta)
        while True:
            con, cliente = self.tcp.accept()
            try:
                con_secure = self.context.wrap_socket(con, server_side=True)
                thread.start_new_thread(self.conectado, tuple([con_secure, cliente]))
            except Exception as e:
                print("Tentativa de acesso invalida..")



servidor= ServidorConexao()
servidor.iniciar_servidor()
