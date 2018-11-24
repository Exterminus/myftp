# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Cliente
Carlos Magno
UFSJ
"""
import sys
import socket
import getpass
#utilizado para serialização de dados..
import pickle
#conexao segura.. todas as conexoes serao segura
import ssl
class Cliente(object):
    """Classe cliente conecta
     ao servido usando tcp"""
    #ip do servidor de conexao
    #self.ip=""
    def __init__(self):
        self.ip_conexao=0
        self.porta=0
        self.tcp_seguro=""
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #conexao segura#-----------------------------------------
        #self.context = ssl.create_default_context()
        self.context = ssl.SSLContext()
        self.context.verify_mode = ssl.CERT_REQUIRED
        #self.context.check_hostname = True
        #Carrega a chave publica do servidor...
        self.context.load_verify_locations('chave_cliente/server.pem')

        self.tcp.settimeout(3)
        self.home=""

    def verifica_comando(self,comando):
        """verifica se o comando esta formatado antes de enviar"""
        particao=comando.split(" ")
        if("newuser" in comando):
            #newuser carlos 4363 0
            if(len(particao)<4):
                return False,None,None,None
            cmd=particao[0]
            user=particao[1]
            senha=particao[2]
            permissao=particao[3]
            return cmd,user,senha,permissao

        if("put" in comando):
            #carrega o arquivo...
            cmd=particao[1]
            try:
                arq=open(cmd,"rb")
                file=arq.read()
                arq.close()
                return True, particao[0],particao[1],file
            except Exception as e:
                print("erro put",e)
                return False,None,None,None
        else:
            #estado,comando,
            if(len(particao)>1):
                return True,particao[0],particao[1],None
            return True,particao[0],None,None

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
        self.tcp_seguro=self.context.wrap_socket(self.tcp)
        #transforma o tcp em uma conexao segura
        self.tcp=self.tcp_seguro
        self.tcp.connect(destino)
        #self.tcp=self.tcp_seguro
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
        """exibe uma lista"""
        if(len(lista)<1):
            print("lista vazia")
        else:
            for i in lista:
                print("-",i)
    def salvar_arquivo(self,nome,file):
        """salva um arquivo, utilizado para get"""
        arquivo=open(nome,"wb")
        #print("File salvar",file)

        arquivo.write(file.data)
        print("transferência concluída.")
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
        elif("put" in resposta):
            if(resposta['put']):
                print("Arquivo enviado com sucesso.")
            else:

                print("Erro ao enviar o arquivo.")
        elif("newuser" in resposta):
            if(resposta['newuser']):
                print("Usuario criado com sucesso.")
            else:
                print("Erro ao criar o usuario.")
                if(resposta['root'] is False):
                    print("Você não é um usuário root!!.")
                    print("Esta ocorrência será relatada!")
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
                comando=""
                comando=input(self.home+">>")
                #comando_inst=pickle.dumps(comando)
                #realiza uma pré verificação do comando digitado.
                #cd casa
                estado,comando_inst,caminho,file=self.verifica_comando(comando)
                #return cmd,user,senha,permissao
                if(estado):
                    if("newuser" in comando):
                        cmd={}
                        cmd['cmd']=estado
                        cmd['user']=comando_inst
                        cmd['senha']=caminho
                        cmd['permissao']=file
                        comando_inst=pickle.dumps(cmd)
                        self.tcp.sendall(comando_inst)
                    else:
                        cmd={}
                        cmd['cmd']=comando_inst
                        cmd['caminho']=caminho
                        cmd['file']=file
                        comando_inst=pickle.dumps(cmd)
                        self.tcp.sendall(comando_inst)
                else:
                    print("verifique o comando digitado.")
                rec=[]
                recebido=0
                while True:
                    #print("entrou")
                    resposta=""
                    #print("w")
                    resposta=self.tcp.recv(1024)
                    rec.append(resposta)
                    #print("P",len(resposta))
                    recebido=len(resposta)-1024
                    if(recebido<0):
                        break
                resposta=pickle.loads(b"".join(rec))
                self.processa_resposta(resposta)
            except Exception as e:
                print(e)
                self.encerrar_conexao()

    def coleta_dados(self):
        """realiza a coleta dos dados de login"""
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
