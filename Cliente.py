# encoding:utf8
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
        print("Mensagem Inicial:",retorno.decode("utf-8"))
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
                comando=input(">> ")
                self.tcp.sendall(comando.encode())
                data = self.tcp.recv(1024)
                print(data.decode("utf8"))
            except Exception as e:
                print(e)
                print('closing socket')
                self.tcp.close()
    def encerrar_conexao(self):
        tcp.close()
cliente=Cliente()
cliente.inicia_conexao(sys.argv[1],sys.argv[2])
senha=cliente.login(sys.argv[3])
if(senha):
    cliente.console()
else:
    print("Não foi possível efetuar o login.")
