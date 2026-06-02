from flask import Blueprint, jsonify, request
from app.services.agente5_sim import Agente5Sim

paquetes_bp = Blueprint('paquetes', __name__)

# Rutas del Módulo de Paquete Turístico
@paquetes_bp.route('/buscar', methods=['GET'])
def buscar():
    destino = request.args.get('destino')
    paquetes = Agente5Sim.buscar_paquetes(destino)
    return jsonify({
        "status": "success",
        "count": len(paquetes),
        "data": paquetes
    })

@paquetes_bp.route('/crear', methods=['POST'])
def crear():
    # Simulación de creación/reserva de paquete
    datos = request.json
    return jsonify({
        "status": "success",
        "message": "Reserva de paquete iniciada",
        "reserva_id": f"PK-RES-54321",
        "datos": datos
    })
