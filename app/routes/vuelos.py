from flask import Blueprint, jsonify, request
from app.services.agente5_sim import Agente5Sim

vuelos_bp = Blueprint('vuelos', __name__)

# Rutas del Módulo de Vuelos
@vuelos_bp.route('/buscar', methods=['GET'])
def buscar():
    origen = request.args.get('origen')
    destino = request.args.get('destino')
    fecha = request.args.get('fecha')
    
    vuelos = Agente5Sim.buscar_vuelos(origen, destino, fecha)
    return jsonify({
        "status": "success",
        "count": len(vuelos),
        "data": vuelos
    })

@vuelos_bp.route('/reserva', methods=['POST'])
def reserva():
    # En una aplicación real, aquí guardaríamos la reserva en la base de datos
    datos = request.json
    return jsonify({
        "status": "success",
        "message": "Reserva iniciada correctamente",
        "reserva_id": f"RES-{12345}",
        "datos": datos
    })
