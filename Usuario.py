class Usuario():
    """docstring for Usuario."""
    def __init__(self,login,root):
        self.login=""
        self.root=""
        self.home="home/"+login+"/"

    def setLogin(self,login):
        self.login=login

    def setPermissao(self,permissao):
        self.root=permissao

    def getLogin(self):
        return self.login

    def getPermissao(self):
        return self.root

    def getHome(self):
        return self.home