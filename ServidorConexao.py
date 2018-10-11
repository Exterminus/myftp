# encoding:utf8
import sys
import socket
import _thread as thread
class ServidorConexao(object):
    """docstring for ServidorConexao."""
    def __init__(self):
        self.porta=5003
        self.ip=""
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.bind((self.ip,self.porta))
        self.tcp.listen(1)

    def processa_comando(self,conexao,comando):
        if(comando.decode("utf-8")=="logout"):
            conexao.sendall(b"conexao encerrada...")
            conexao.close()
            thread.exit()

    def conectado(self,connection, cliente):
        connection.sendall(b'Bem vindo ao Zeus FTP')
        while True:
            # Wait for a connection
            try:
                print('connection from', cliente)
                # Receive the data in small chunks and retransmit it
                data = connection.recv(1024)
                print(data)
                print('received {!r}'.format(data))
                self.processa_comando(connection,data)
                if data:
                    print('sending data back to the client')
                    connection.sendall(data)
                else:
                    print('no data from', cliente)
                    break
            except Exception as e:
                # Clean up the connection
                print("e",e)
                connection.close()
                thread.exit()
    def iniciar_servidor(self):
        print("Servidor Iniciado..")
        while True:
            con, cliente = self.tcp.accept()
            thread.start_new_thread(self.conectado, tuple([con, cliente]))


servidor= ServidorConexao()
servidor.iniciar_servidor()
