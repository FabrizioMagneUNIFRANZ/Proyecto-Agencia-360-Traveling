from flask import Blueprint, jsonify, request, current_app
from app.models.usuario import Usuario
from app.models.reserva import PaqueteTuristico, ReservaVuelo, ReservaHotel, ReservaTraslado, Cliente, Empleado
from app.routes.auth import token_required
from app import db
from sqlalchemy import func
import datetime
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(current_user, *args, **kwargs):
        if current_user.rol != 'administrador':
            return jsonify({'message': 'Se requieren privilegios de administrador'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

def agent_required(f):
    @wraps(f)
    @token_required
    def decorated(current_user, *args, **kwargs):
        if current_user.rol not in ['agente', 'administrador']:
            return jsonify({'message': 'Se requieren privilegios de agente o administrador'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# --- DASHBOARD Y REPORTES (Para Agentes y Admin) ---

@admin_bp.route('/dashboard/servicios', methods=['GET'])
@agent_required
def dashboard_servicios(current_user):
    # Simulación de obtención de datos para el dashboard
    vuelos_count = ReservaVuelo.query.count()
    hoteles_count = ReservaHotel.query.count()
    paquetes_count = PaqueteTuristico.query.count()
    traslados_count = ReservaTraslado.query.count()
    
    return jsonify({
        "vuelos": vuelos_count,
        "hoteles": hoteles_count,
        "paquetes": paquetes_count,
        "traslados": traslados_count,
        "message": "Datos del dashboard obtenidos correctamente"
    })

@admin_bp.route('/reportes/mensual', methods=['GET'])
@agent_required
def reporte_mensual(current_user):
    mes = request.args.get('mes', datetime.datetime.now().month)
    anio = request.args.get('anio', datetime.datetime.now().year)
    
    # Simulación de reporte de ventas/reservas por mes
    ventas_totales = db.session.query(func.sum(PaqueteTuristico.precio_total)).filter(
        func.extract('month', PaqueteTuristico.fecha_creacion) == mes,
        func.extract('year', PaqueteTuristico.fecha_creacion) == anio
    ).scalar() or 0
    
    return jsonify({
        "mes": mes,
        "anio": anio,
        "ventas_totales": float(ventas_totales),
        "moneda": "USD"
    })

# --- GESTIÓN DE USUARIOS (Solo Admin) ---

@admin_bp.route('/usuarios', methods=['GET'])
@admin_required
def listar_usuarios(current_user):
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])

@admin_bp.route('/usuarios/<int:id>', methods=['PUT'])
@admin_required
def modificar_usuario(current_user, id):
    user = Usuario.query.get_or_404(id)
    data = request.json
    
    if 'rol' in data:
        user.rol = data['rol']
    if 'estado' in data:
        user.estado = data['estado']
    if 'correo' in data:
        user.correo_usuario = data['correo']
        
    db.session.commit()
    return jsonify({"message": "Usuario actualizado", "user": user.to_dict()})

@admin_bp.route('/usuarios/<int:id>', methods=['DELETE'])
@admin_required
def eliminar_usuario(current_user, id):
    user = Usuario.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado correctamente"})

# --- SUPERVISIÓN DE VENTAS POR AGENTE (Solo Admin) ---

@admin_bp.route('/supervision/ventas-agentes', methods=['GET'])
@admin_required
def supervision_ventas(current_user):
    # Consulta para agrupar ventas por empleado (agente)
    ventas_por_agente = db.session.query(
        Empleado.primer_nombre, 
        Empleado.apellido_paterno,
        func.count(PaqueteTuristico.id_paquete_turistico).label('total_paquetes'),
        func.sum(PaqueteTuristico.precio_total).label('monto_total')
    ).join(PaqueteTuristico, Empleado.id_empleado == PaqueteTuristico.id_empleado)\
     .group_by(Empleado.id_empleado).all()
     
    resultado = []
    for v in ventas_por_agente:
        resultado.append({
            "agente": f"{v.primer_nombre} {v.apellido_paterno}",
            "total_paquetes": v.total_paquetes,
            "monto_total": float(v.monto_total or 0)
        })
        
    return jsonify(resultado)
