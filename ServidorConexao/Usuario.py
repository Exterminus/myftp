# -*- coding: utf-8 -*-
#!/usr/bin/env python3

"""
Classe do usuário.
"""
class Usuario():
    """docstring for Usuario."""
    def __init__(self,login,root):
        self.login=login
        self.root=root
        self.home="home/"+login+"/"

    def setLogin(self,login):
        self.login=login

    def setPermissao(self,permissao):
        if("True" in permissao):
            self.root=True
        else:
            self.root=False

    def getLogin(self):
        return self.login

    def getPermissao(self):
        return self.root

    def getHome(self):
        return self.home

    def setHome(self,caminho):
        self.home=caminho
