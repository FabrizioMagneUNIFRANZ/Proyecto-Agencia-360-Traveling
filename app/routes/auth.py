from flask import Blueprint, jsonify, request, current_app
from app.models.usuario import Usuario
from app.models.reserva import Cliente, Empleado
from app import db
import jwt
import datetime
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Usuario.query.filter_by(id_usuario=data['id_usuario']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Rutas del Módulo de Administración (Usuarios)
@auth_bp.route('/login', methods=['POST'])
def login():
    auth = request.json
    if not auth or not auth.get('correo') or not auth.get('password'):
        return jsonify({"message": "Faltan credenciales"}), 400

    user = Usuario.query.filter_by(correo_usuario=auth.get('correo')).first()
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    if user.check_password(auth.get('password')):
        token = jwt.encode({
            'id_usuario': user.id_usuario,
            'rol': user.rol,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            'token': token,
            'user': user.to_dict()
        })

    return jsonify({"message": "Contraseña incorrecta"}), 401

@auth_bp.route('/registro', methods=['POST'])
def registro():
    data = request.json
    
    # Validar datos básicos
    if not data.get('correo') or not data.get('password') or not data.get('rol'):
        return jsonify({"message": "Datos incompletos"}), 400
    
    # Verificar si el usuario ya existe
    if Usuario.query.filter_by(correo_usuario=data.get('correo')).first():
        return jsonify({"message": "El correo ya está registrado"}), 409
    
    try:
        nuevo_usuario = Usuario(
            correo_usuario=data.get('correo'),
            rol=data.get('rol'),
            fecha_registro=datetime.datetime.utcnow().date()
        )
        nuevo_usuario.set_password(data.get('password'))
        
        db.session.add(nuevo_usuario)
        db.session.flush() # Para obtener el id_usuario
        
        # Crear perfil asociado (Cliente o Empleado)
        if nuevo_usuario.rol == 'cliente':
            nuevo_perfil = Cliente(
                id_usuario=nuevo_usuario.id_usuario,
                ci=data.get('ci', ''),
                primer_nombre=data.get('nombre', ''),
                apellido_paterno=data.get('apellido', ''),
                fecha_nacimiento=datetime.datetime.strptime(data.get('fecha_nacimiento', '2000-01-01'), '%Y-%m-%d').date(),
                correo=data.get('correo')
            )
            db.session.add(nuevo_perfil)
        elif nuevo_usuario.rol in ['agente', 'administrador']:
            nuevo_perfil = Empleado(
                id_usuario=nuevo_usuario.id_usuario,
                ci=data.get('ci', ''),
                primer_nombre=data.get('nombre', ''),
                apellido_paterno=data.get('apellido', ''),
                fecha_nacimiento=datetime.datetime.strptime(data.get('fecha_nacimiento', '2000-01-01'), '%Y-%m-%d').date()
            )
            db.session.add(nuevo_perfil)
            
        db.session.commit()
        return jsonify({"message": "Usuario registrado exitosamente", "user": nuevo_usuario.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al registrar: {str(e)}"}), 500

@auth_bp.route('/perfil', methods=['GET'])
@token_required
def perfil(current_user):
    return jsonify({
        "user": current_user.to_dict(),
        "message": "Perfil obtenido correctamente"
    })
