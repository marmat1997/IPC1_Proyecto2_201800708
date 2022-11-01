from flask import Flask, jsonify, request
from flask_cors import CORS
from usuario import Usuario
from publicacion import Publicacion
from datetime import datetime

Usuarios = []
Publicaciones = []
contadorPublicaciones = 100
Usuarios.append(Usuario(1,'marvin','admin','1234'))
app = Flask(__name__)
CORS(app)


# funcion para obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def usuarios():
    global Usuarios
    Datos = []
    for u in Usuarios:
        dato = {
            "id": u.getId(),
            "nombre": u.getNombre(),
            "nickname": u.getnickname(),
            "password": u.getPassword()
        }
        Datos.append(dato)
    respuesta = jsonify(Datos)
    return (respuesta)

# funcion para agregar usuarios
@app.route('/agregarUsuario', methods=['POST'])
def AgregarUsuario():
    global Usuarios
    id = request.json['id']
    name = request.json['name']
    nickname = request.json['nickname']
    password = request.json['password']
    bandera_id = False
    bandera_nickname = False

    for u in Usuarios:
        if u.getId() == id:
            bandera_id = True
            break

    for u in Usuarios:
        if u.getnickname() == nickname:
            bandera_nickname = True
            break
    if bandera_id:
        return jsonify({
            'status': '015',
            'msg': 'id ya existente'
            })
    else:
        if bandera_nickname:
            return jsonify({
                'status': '020',
                'msg': 'nickname ya existente'
                })
        else:
            nuevo = Usuario(id, name, nickname, password)
            Usuarios.append(nuevo)
            return jsonify({
                'status': '025',
                'msg': 'Usuario Creado'
                })
            

# FUncion para realizar el login


@app.route('/login', methods=['POST'])
def login():
    username = request.json['nickname']
    password = request.json['password']
    bandera = False
    for u in Usuarios:
        if u.getnickname() == username:
            bandera = True
            break
    if bandera:
        for u in Usuarios:
            if u.getnickname() == username:
                if u.getPassword() == password:
                    return jsonify({
                        'status': '200',
                        'msg': 'Credenciales Correctas'
                        })
                else:
                    return jsonify({
                        'status': '010',
                        'msg': 'contraseña incorrecta'
                        })
    else:
        return jsonify({
            'status': '005',
            'msg': 'Usuario no registrado'
            })

# funcion para buscar un usuario


@app.route('/buscar/<string:nickname>', methods=['GET'])
def buscar(nickname):
    global Usuarios
    Datos = []
    respuesta = jsonify(Datos)
    bandera = False
    for u in Usuarios:
        if u.getnickname() == nickname:
            dato = {
                "id": u.getId(),
                "nombre": u.getNombre(),
                "nickname": u.getnickname(),
                "password": u.getPassword()
            }
            Datos.append(dato)
            respuesta = jsonify(Datos)
            bandera = True
            break
    if bandera:
        return respuesta
    else:
        return jsonify({
            'status': '006',
            'msg': 'Usuario no registrado'
            })

# funcion para modificar un usuario


@app.route('/modificar/<string:nickname>', methods=['PUT'])
def modificarUsuario(nickname):
    global Usuarios
    bandera = False
    for u in Usuarios:
        if u.getnickname() == nickname:
            u.setId(request.json['id'])
            u.setNombre(request.json['name']),
            u.setnickname(request.json['nickname']),
            u.setPassword(request.json['password'])
            bandera = True
            break      

    if bandera:
        return jsonify({
            'status': '030',
            'msg': 'Se ha actualizado los datos exitosamente'
            })
    else:
        return jsonify({
            'status': '031',
            'msg': 'No se pudo Actualizar los datos'
            })

# Funcion para eliminar un usuario


@app.route('/eliminar/<string:nickname>', methods=['DELETE'])
def eliminarUsuario(nickname):
    global Usuarios
    bandera = False
    for i in range(len(Usuarios)):
        if Usuarios[i].getnickname() == nickname:
            del Usuarios[i]
            bandera = True
            break
    if bandera:
        return jsonify({
            'status': '050',
            'msg': 'Se eliminó el usuario exitosamente'
            })
    else:
        return jsonify({
            'status': '049',
            'msg': 'Error al eliminar el usuario'
            })

# funcion para agregar varios usuarios


@app.route('/cargaUsuarios', methods=['POST'])
def cargaUsuarios():
    global Usuarios
    arg = request.json['name'].split()
    if (len(arg) == 2):
        nombre = arg[0]
        apellido = arg[1]
    else:
        nombre = arg[0]
        apellido = ""

    genero = request.json['gender']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    bandera_correo = False
    bandera_usuario = False
    for u in Usuarios:
        if u.getEmail() == email:
            bandera_correo = True
            break

    for u in Usuarios:
        if u.getUsername() == username:
            bandera_usuario = True
            break
    if bandera_correo:
        return jsonify({
            'status': '015',
            'msg': 'Correo ya existente'
            })
    else:
        if bandera_usuario:
            return jsonify({
                'status': '020',
                'msg': 'Usuario ya existente'
                })
        else:
            if len(password) >= 8:
                if numero(password):
                    if simbolo(password):
                        nuevo = Usuario(nombre, apellido, genero,
                                        username, email, password)
                        Usuarios.append(nuevo)
                        return jsonify({
                            'status': '025',
                            'msg': 'Credenciales Correctas'
                            })
                    else:
                        return jsonify({
                            'status': '021',
                            'msg': 'el password tiene que tener como minimo 1 simbolo'
                        })
                else:
                    return jsonify({
                        'status': '022',
                        'msg': 'el password tiene que tener como minimo 1 numero'
                    })
            else:
                return jsonify({
                    'status': '023',
                    'msg': 'el password tiene que tener como minimo 8 caracteres'
                })


# funcion para agregar usuarios
@app.route('/imgPublicaciones', methods=['POST'])
def agregarPublicaciones():
    global Publicaciones
    global contadorPublicaciones
    tipo = "image"
    categoria = request.json['category']
    author = request.json['author']
    url = request.json['url']
    date = request.json['date']
    bandera_usuario = False

    for u in Usuarios:
        if u.getUsername() == author:
            bandera_usuario = True
            break
    if bandera_usuario:

        nuevo = Publicacion(contadorPublicaciones, tipo,
                            categoria, author, url, date)
        contadorPublicaciones = contadorPublicaciones+1
        Publicaciones.append(nuevo)
        return jsonify({
            'status': '060',
            'msg': 'Publicacion Guardada'
        })
    else:
        return jsonify({
            'status': '061',
            'msg': 'Error al subir la publicacion Author no registrado'
        })

# funcion para agregar publicaciones videos


@app.route('/vidPublicaciones', methods=['POST'])
def agregarVPublicaciones():
    global Publicaciones
    global contadorPublicaciones
    tipo = "videos"
    categoria = request.json['category']
    author = request.json['author']
    urlTemp = request.json['url']
    arg = urlTemp.split(sep='/')
    url = arg[0]+'//www.youtube.com'+'/embed/'+arg[3]
    print(url)
    date = request.json['date']
    bandera_usuario = False

    for u in Usuarios:
        if u.getUsername() == author:
            bandera_usuario = True
            break
    if bandera_usuario:
        nuevo = Publicacion(contadorPublicaciones, tipo,
                            categoria, author, url, date)
        contadorPublicaciones = contadorPublicaciones+1
        Publicaciones.append(nuevo)
        return jsonify({
            'status': '060',
            'msg': 'Publicacion Guardada'
        })
    else:
        return jsonify({
            'status': '061',
            'msg': 'Error al subir la publicacion Author no registrado'
        })

# funcion para obtener todas las publicaciones


@app.route('/publicaciones', methods=['GET'])
def publicaciones():
    global Publicaciones
    Datos = []
    for u in Publicaciones:
        dato = {
            "id": u.getId(),
            "tipo": u.getTipo(),
            "categoria": u.getCategoria(),
            "author": u.getAuthor(),
            "date": u.getDate(),
            "url": u.getUrl()
        }
        Datos.append(dato)
    respuesta = jsonify(Datos)
    return (respuesta)

# Funcion para eliminar una publicacion


@app.route('/eliminarPb/<int:id>', methods=['DELETE'])
def eliminarPublicacion(id):
    global Publicaciones
    bandera = False
    for i in range(len(Publicaciones)):
        if Publicaciones[i].getId() == id:
            del Publicaciones[i]
            bandera = True
            break
    if bandera:
        return jsonify({
            'status': '062',
            'msg': 'Se eliminó la publicacion exitosamente'
            })
    else:
        return jsonify({
            'status': '063',
            'msg': 'Error al eliminar la publicacion'
            })

#publicacion nueva individual
@app.route('/publicarNew', methods=['POST'])
def nuevaPublicacion():
    global Publicaciones
    global contadorPublicaciones
    tipo = request.json['tipo']
    categoria = request.json['categoria']
    author = request.json['author']
    urlTemp = request.json['url']
    if (tipo=="image"):
        url = urlTemp
        date = datetime.today().strftime('%d/%m/%Y')
        nuevo = Publicacion(contadorPublicaciones, tipo,categoria, author, url, date)
        contadorPublicaciones=contadorPublicaciones+1
        Publicaciones.append(nuevo)
        return jsonify({
            'status':'060',
            'msg':'Publicacion Guardada'
        })
    else:
        arg = urlTemp.split(sep='/')
        url = arg[0]+'//www.youtube.com'+'/embed/'+arg[3]
        date = datetime.today().strftime('%d/%m/%Y')
        nuevo = Publicacion(contadorPublicaciones, tipo,categoria, author, url, date)
        contadorPublicaciones=contadorPublicaciones+1
        Publicaciones.append(nuevo)
        return jsonify({
            'status':'060',
            'msg':'Publicacion Guardada'
        })


if __name__ == "__main__":
    app.run(threaded=True, debug=True, port=4000)
