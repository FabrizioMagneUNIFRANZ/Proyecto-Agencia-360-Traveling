from flask import Blueprint, jsonify, request

auth_bp = Blueprint('auth', __name__)

# Rutas del Módulo de Administración (Usuarios)
@auth_bp.route('/login', methods=['POST'])
def login():
    return jsonify({"message": "Endpoint de login (Próximamente)"})

@auth_bp.route('/registro', methods=['POST'])
def registro():
    return jsonify({"message": "Endpoint de registro de usuario (Próximamente)"})

@auth_bp.route('/perfil', methods=['GET'])
def perfil():
    return jsonify({"message": "Endpoint para obtener datos del perfil del usuario (Próximamente)"})
