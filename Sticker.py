class Sticker:
    def __init__(self,id, nombre, apellido, seleccion, region,imagen):
        self.id=id
        self.nombre=nombre
        self.apellido=apellido
        self.seleccion=seleccion
        self.imagen=imagen    
        self.region=region

    def getId(self):
        return self.id

    def getNombre (self):
        return self.nombre
    
    def getApellido(self):
        return self.apellido
    
    def getSeleccion(self):
        return self.seleccion
    
    def getRegion (self):
        return self.region
    
    def getImagen (self):
        return self.imagen
    
    def setNombre (self, nombre):
        self.nombre=nombre
    
    def setApellido(self, apellido):
        self.apellido=apellido
    
    def setSeleccion (self, seleccion):
        self.seleccion=seleccion
    
    def setRegion (self,region):
        self.region=region