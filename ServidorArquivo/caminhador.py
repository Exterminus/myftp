# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import os
caminho=["home"]

def gera_caminho(lista):
    return "/".join(lista)
while True:

    comando=input(">>> ")
    if("cd .." in comando):
        print("break")
        print("Quit",caminho.pop())
        comando=""
        #exit()
    caminho.append(comando)

    print("Caminho",gera_caminho(caminho))
    print("Files...",os.listdir(gera_caminho(caminho)))
