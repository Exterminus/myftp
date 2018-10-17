# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Cliente
"""
import sys
import socket
import getpass
#utilizado para serialização de dados..
import pickle
class Cliente(object):
    """Classe cliente conecta
     ao servido usando tcp"""
    #ip do servidor de conexao
    #self.ip=""
    def __init__(self):
        self.ip_conexao=0
        self.porta=0
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def valida_dados(self,ip,porta):
        pass

    def login(self,usuario):
        """Realiza o pedido de Login"""
        print("Dados conexão\nIP:",self.ip_conexao,"Porta:",self.porta,"Usuario:",usuario)
        senha=getpass.getpass("senha: ")
        #print("IP:",self.ip_conexao,"Porta:",self.porta,"Usuario:",usuario,"senha:",senha)
        msg={"usuario":usuario,"senha":senha}
        #dicionario é serializado em bytes..
        msg_b=pickle.dumps(msg)
        self.tcp.sendall(msg_b)
        retorno=self.tcp.recv(1024)
        #print("Retorno",pickle.loads(retorno))
        if(pickle.loads(retorno)):
            return True
        else:
            return False

    def inicia_conexao(self,ip,porta):
        """Inicia a conexão com servidor."""
        self.ip_conexao=ip
        self.porta = porta
        destino=(self.ip_conexao,int(self.porta))
        self.tcp.connect(destino)
        retorno=self.tcp.recv(1024)
        retorno=pickle.loads(retorno)
        print("Mensagem Inicial:",retorno)

    def encerrar_conexao(self):
        """encerra a conexão com o servidor de conexão"""
        print("Conexão encerrada.\nBye.")
        self.tcp.close()
        exit(-1)

    def exibe_lista(self,lista):
        for i in lista:
            print("-",i)

    def processa_resposta(self,resposta):
        """processa a resposta recebida do servidor"""
        if(resposta is True or resposta is None):
            print(resposta)

        if("rmdir" in resposta):
            #print(resposta['rmdir'])
            if(resposta['rmdir'] is True):
                print(resposta['rmdir'])
                print("diretório removido")
            else:
                print("erro ao remover o diretório.")
        elif("mkdir" in resposta):
            #print(resposta['mkdir'])
            if(resposta['mkdir'] is True):
                print(resposta['mkdir'])
                print("diretório criado")
            else:
                print("erro ao criar o diretório.")
        elif("logout" in resposta):
            self.encerrar_conexao()
        elif("ls" in resposta):
            self.exibe_lista(resposta['ls'])
        else:
            print(resposta)

    def console(self):
        """Inicia o console de comandos"""
        #print("Digite a sua mensagem   ")
        while(True):
            try:
                # # Send data
                # message = b'This is the message.  It will be repeated.'
                # print('sending {!r}'.format(message))
                # self.tcp.sendall(message)
                # Look for the response
                comando=""
                comando=input(">> ")
                comando_inst=pickle.dumps(comando)
                self.tcp.sendall(comando_inst)
                resposta = self.tcp.recv(1024)
                #print(resposta.decode("utf8"))
                resposta=pickle.loads(resposta)
                self.processa_resposta(resposta)
            except Exception as e:
                print(e,pickle.loads(comando_inst),resposta)
                # print('closing socket')
                # self.tcp.close()
                self.encerrar_conexao()
cliente=Cliente()
cliente.inicia_conexao(sys.argv[1],sys.argv[2])
senha=cliente.login(sys.argv[3])
if(senha):
    cliente.console()
else:
    print("Não foi possível efetuar o login.")
