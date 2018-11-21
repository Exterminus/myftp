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
        self.home=""

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
        retorno=pickle.loads(retorno)
        if(retorno['estado']):
            #retorna a mensagem de sucesso de login e o caminho da home
            return True,retorno['home']
        else:
            return False,False

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
    ##---------------------
    def exibe_lista(self,lista):
        if(len(lista)<1):
            print("lista vazia")
        else:
            for i in lista:
                print("-",i)
    def salvar_arquivo(self,nome,file):
        arquivo=open(nome,"wb")
        arquivo.writelines(file)
        arquivo.close()
    ##-------------------------------------
    def processa_resposta(self,resposta):
        """processa a resposta recebida do servidor"""
        if(resposta is True or resposta is None):
            print(resposta)

        if("rmdir" in resposta):
            #print(resposta['rmdir'])
            if(resposta['rmdir'] is True):
                #print(resposta['rmdir'])
                print("diretório removido")
            else:
                print("erro ao remover o diretório.")
        elif("delete" in resposta):
            #print(resposta['rmdir'])
            if(resposta['delete'] is True):
                #print(resposta['delete'])
                print("arquivo removido")
            else:
                print("erro ao remover o arquivo.")
        elif("mkdir" in resposta):
            #print(resposta['mkdir'])
            if(resposta['mkdir'] is True):
                print(resposta['mkdir'])
                print("diretório criado")
            else:
                print("erro ao criar o diretório.")
        elif("quit" in resposta):
            self.encerrar_conexao()
        elif("get" in resposta):
            if(resposta['get']):
                self.salvar_arquivo(resposta['nome'],resposta['file'])
        elif("ls" in resposta):
            self.exibe_lista(resposta['ls'])
        elif("cd" in resposta):
            if(resposta['cd']):
                #atualiza o caminho da home
                self.home=resposta['home']
                #print(self.home)
        else:
            print(resposta)

    def console(self,home):
        """Inicia o console de comandos"""
        #print("Digite a sua mensagem   ")
        self.home=home
        while(True):
            try:
                # # Send data
                # message = b'This is the message.  It will be repeated.'
                # print('sending {!r}'.format(message))
                # self.tcp.sendall(message)
                # Look for the response
                comando=""
                comando=input(self.home+">>")
                #print("CMD",comando)
                comando_inst=pickle.dumps(comando)
                self.tcp.sendall(comando_inst)
                rec=[]
                try:
                    resposta1 = self.tcp.recv(4096)
                    rec.append(resposta1)
                    resposta=pickle.loads(b"".join(rec))
                except Exception as e:
                    while True:
                        resposta2=self.tcp.recv(4096)
                        rec.append(resposta2)
                        if not resposta2:
                            break
                    resposta=pickle.loads(b"".join(rec))

                #resposta = []
                # try:
                #     packet = self.tcp.recv(4096)
                #     resposta.append(packet)
                # except Exception as e:
                #     exit()

                    #print(len(packet))
                #print(resposta.decode("utf8"))
                #resposta=pickle.loads(resposta)
                self.processa_resposta(resposta)
            except Exception as e:
                print(e,pickle.loads(comando_inst),resposta)
                # print('closing socket')
                # self.tcp.close()
                self.encerrar_conexao()
    def coleta_dados(self):
        try:
            ip=sys.argv[1]
            porta=sys.argv[2]
            login=sys.argv[3]
        except Exception as e:
            print("Erro!\nDigite:\nip porta login\n")
            exit()
        return ip,porta,login
cliente=Cliente()
ip,porta,login=cliente.coleta_dados()
cliente.inicia_conexao(ip,porta)
senha,home=cliente.login(login)
if(senha):
    cliente.console(home)
else:
    print("Não foi possível efetuar o login.")
