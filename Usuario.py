class Usuario:
    def __init__(self,id,name,nickName,password):
        self.name=name
        self.id=id
        self.nickName=nickName
        self.password=password
        self.sticker=[]

    def getId(self):
        return self.id
    def getName(self):
        return self.name
    def getNickName(self):
        return self.nickName
    def getPassword(self):
        return self.password
    def getSticker(self):
        return self.sticker

   
    def setId(self,id):
        self.id=id
    def setName(self,name):
        self.name=name
    
    def setNickName(self,nickName):
        self.nickName=nickName

    def setPassword(self,password):
        self.password=password

   