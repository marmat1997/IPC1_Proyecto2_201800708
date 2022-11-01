from tkinter import image_names
from flask import Flask,request
from flask import render_template,url_for,jsonify
from flask_cors import CORS
from flask.wrappers import Response
from Usuario import Usuario
from Sticker import Sticker

LUsuarios=[]
LUsuarios.append(Usuario("1","marvin","marmat","123"))



app=Flask(__name__)
cors=CORS(app,resources={r"/*":{"origin":"*"}})

@app.route('/', methods=['GET'] )
def inicio():
    return render_template('Inicio.html')

@app.route('/Inicio', methods=['GET'] )
def inicio2():
    return render_template('Inicio.html')
    


@app.route('/Principal', methods=['GET'] )
def Principal():
    return render_template('Principal.html')

@app.route('/Editar', methods=['GET'] )
def rutaModificar():
    return render_template('modificar.html')

@app.route('/Registrar', methods=['GET'] )
def Registrar():
    return render_template('registro.html')
    


@app.route('/CUsuario', methods=['POST'] ) #recibe datos
def agregarUsuario():
    global LUsuarios
    ids=request.json['id']
    nameUs=request.json['nombre']
    nickName=request.json['nickName']
    password=request.json['password']
    banderas=False
    for usuarios in LUsuarios:
        if usuarios.getNickName()==nickName:
            banderas=True
            break
        else:
            banderas=False
    if banderas==False:
        nuevo=Usuario(ids,nameUs,nickName,password)
        LUsuarios.append(nuevo)
        print(LUsuarios)
        return jsonify({
         'message':'Success',
         'reason':'Usuario Agregado',
         'status': 200
         }) 
    else:
        return jsonify({
         'message':'Filed',
         'reason':'Usuario ya registrado',
         'status': 400
         }) 

    

    # return 'registro exitoso'

@app.route('/Login', methods=['POST'] ) #recibe datos
def login():
     global LUsuarios
     nickName=request.json['user_nickname']
     password=request.json['user_password']
     for usuarios in LUsuarios:
        if usuarios.getNickName()==nickName and usuarios.getPassword()==password:
            bandera=True
            break
        else:
            bandera=False
     if bandera==True:
        return jsonify({
         'message':'Success',
         'reason':'Usuario Agregado',
         'status': 200
         })

     else:
        return jsonify({
         'message':'Failed',
         'reason':'Usuario no registrado',
         'status': 400
         })

      
    

    # return 'registro exitoso'
    

@app.route('/Usuarios', methods=['GET'] ) #manda datos
def MostrarUsuarios():
    lista=[]
    global LUsuarios
    for usuario in LUsuarios:
        aux= { 
           'id_user':usuario.getId(),
           'user_name':usuario.getName(),
           'user_nickname':usuario.getNickName(),
           'user_password':usuario.getPassword()
            }
        lista.append(aux)

    respuesta=jsonify(lista)
    return (respuesta)



@app.route('/Stickers/<string:nombre>', methods=['GET'])
def ObtenerSticker(nombre):
    global LUsuarios
    lista=[]
    for st in LUsuarios:
        if st.getNickName() == nombre:
            for st2 in st.getSticker(): 
                aux= { 
                    'id':st2.getId(),
                    'nombre':st2.getNombre(),
                    'apellido':st2.getApellido(),
                    'equipo':st2.getSeleccion(),
                    'region':st2.getRegion(),
                    'imagen':st2.getImagen()
                     }
                lista.append(aux)
            break
    respuesta = jsonify(lista)
    return(respuesta)

@app.route('/MUsuario/<string:nombre>', methods=['GET'])
def ModificarUsuario(nombre):
    global LUsuarios
    for st2 in LUsuarios:
        if st2.getNickName()==nombre:
            aux= { 
                'id':st2.getId(),
                'nombre':st2.getName(),
                'nickName':st2.getNickName(),
                'password':st2.getPassword()
                 }
            respuesta = jsonify(aux)
            break
            
    return(respuesta)

@app.route('/MUsuario/<string:nombre>', methods=['PUT'])
def ActualizarUsuario(nombre):
    global LUsuarios
    encontra=False
    print(nombre)
    if request.json['estado']=='1':
        for i in range(len(LUsuarios)):
             if request.json['nickName'] == LUsuarios[i].getNickName():
                 encontra=True
                 break    
        if encontra:
            return jsonify({
                  'message':'Existe',
                  'reason':'Usuario ya registrado'
                  }) 
        else:
            for i in range(len(LUsuarios)):
                if nombre == LUsuarios[i].getNickName():
                    LUsuarios[i].setId(request.json['id'])
                    LUsuarios[i].setName(request.json['nombre'])
                    LUsuarios[i].setNickName(request.json['nickName'])
                    LUsuarios[i].setPassword(request.json['password'])
                    
                    break

        
    else:                      
        for i in range(len(LUsuarios)):
            if nombre == LUsuarios[i].getNickName():
                LUsuarios[i].setId(request.json['id'])
                LUsuarios[i].setName(request.json['nombre'])
                LUsuarios[i].setNickName(request.json['nickName'])
                LUsuarios[i].setPassword(request.json['password'])
                break

    return jsonify({'message':'Se actualizo el dato exitosamente'})


@app.route('/cargaSt/<string:valort>', methods=['POST'])
def cargaSticker(valort):
    global LUsuarios
    id=""
    id = request.json['id_sticker']+""
    nombre = request.json['sticker_player_name']
    apellido = request.json['sticker_player_lastname']
    seleccion = request.json['sticker_team']
    imagen= request.json['sticker_region']
    region= request.json['sticker_image']

    
    for u in LUsuarios:
        if u.getNickName() == valort:
            if len(u.getSticker()) >0:
                for s in u.getSticker():
                    if s.getId() == id:
                        pass
                    else:
                        nuevo = Sticker(id,nombre,apellido,seleccion,imagen,region)
                        u.sticker.append(nuevo)
                        print('siuu')
                        break
            else:
                nuevo = Sticker(id,nombre,apellido,seleccion,imagen,region)
                u.sticker.append(nuevo)
                print('siuu')
    return jsonify({
        'status': '025',
        'msg': 'Sticker cargado'
        })




        



if __name__ == "__main__":
    app.run( threaded=True, debug=True,)