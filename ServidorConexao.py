# encoding:utf8
import sys
import socket
import _thread as thread
import getpass
import xmlrpc.client
import pickle
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

    def rpc_senha(self,usuario,senha):
        """Valida a senha e usuario"""
        print(usuario,senha)
        try:
            retorno=self.senha_auth.login(usuario,senha)
            if(retorno):
                #devolve a resposta de login sucesso
                return True
            else:
                return False
        except xmlrpc.client.Fault as err:
            print("Ocorreu um erro")
            print("Código de erro %d" % err.faultCode)
            print("Fault string: %s" % err.faultString)

    def processa_comando(self,conexao,comando):
        #encerra a conexao com o cliente
        if(comando.decode("utf-8")=="logout"):
            conexao.sendall(b"-1")
            conexao.close()
            thread.exit()


    def conectado(self,connection, cliente):
        """verificar o disparo e encerramento de threads"""
        connection.sendall(b'Bem vindo ao Zeus FTP v 1.0 2018.')
        estado_login=False
        data=connection.recv(1024)
        dados_login=pickle.loads(data)
        if(self.rpc_senha(dados_login['usuario'],dados_login['senha'])):
            estado_login=True
            #sucesso ao realizar o login
            connection.sendall(pickle.dumps(True))
        else:
            #erro ao efetuar o login
            connection.sendall(b"False")
        if(estado_login== True):
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
        print("Servidor Iniciado.. na porta",self.porta)
        while True:
            con, cliente = self.tcp.accept()
            thread.start_new_thread(self.conectado, tuple([con, cliente]))


servidor= ServidorConexao()
servidor.iniciar_servidor()
