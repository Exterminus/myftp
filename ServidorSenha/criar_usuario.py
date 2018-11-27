# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from pymongo import MongoClient
import crypt

client= MongoClient('localhost',27017)
#banco de dados da aplicação
db=client.zeus
#colecao onde as senhas estão armazenadas
colecao=db.senhas

def novo_usuario(usuario,senha,root):
    """Cria e insere um usuário no banco"""
    if("True" in root):
        estado=1
    else:
        estado=""
    dados={"login":usuario,"senha":crypt.crypt(senha),"root":bool(estado)}
    try:
        colecao.insert_one(dados)
        #sucesso ao criar um usuário.
        return True
    except Exception as e:
        print("erro ao criar o usuário")
        print(e)
        return False


estado=novo_usuario("zeus","4363","True")
if(estado):
    print("Usuario criado com sucesso")
