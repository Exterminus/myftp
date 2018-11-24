#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def verifica_comando(comando):
    """verifica se o comando esta formatado antes de enviar"""
    particao=comando.split(" ")
    if("put" in comando):
        cmd=particao[1]
        try:
            arq=open(cmd,"rb")
            file=arq.read()
            arq.close()
            return True, particao[0],particao[1],file
        except Exception as e:
            #print(e)
            return False,None
    else:
        return True,None

while True:
    cmd=input(">> ")
    estado,comando,nome,file=verifica_comando(cmd)
    if(estado):
        print("chamando servidor, com0ando ok")
        print(comando,nome)
    else:
        print("erro ao processar o comando.")
