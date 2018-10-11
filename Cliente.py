# encoding:utf8
import sys
import socket
class Cliente(object):
    """Classe cliente conecta
     ao servido usando tcp"""
    #ip do servidor de conexao
    #self.ip=""
    def __init__(self):
        #self.ip_conexao=0
        #self.porta=0
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def inicia_conexao(self,ip,porta):
        """Inicia a conexão com servidor."""
        self.ip_conexao=ip
        self.porta=porta
        destino=(self.ip_conexao,int(self.porta))
        self.tcp.connect(destino)

    def console(self):
        print("Digite a sua mensagem")
        while(True):
            try:
                # # Send data
                # message = b'This is the message.  It will be repeated.'
                # print('sending {!r}'.format(message))
                # self.tcp.sendall(message)
                # Look for the response
                data = self.tcp.recv(1024)
                print(repr(data))
                comando=input()
                self.tcp.sendall(comando.encode())
            except Exception as e:
                print(e)
                print('closing socket')
                self.tcp.close()
    def encerrar_conexao(self):
        tcp.close()
cliente=Cliente()
cliente.inicia_conexao(sys.argv[1],sys.argv[2])
cliente.console()
