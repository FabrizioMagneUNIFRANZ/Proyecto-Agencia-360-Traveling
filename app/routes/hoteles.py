from flask import Blueprint, jsonify, request
from app.services.agente5_sim import Agente5Sim

hoteles_bp = Blueprint('hoteles', __name__)

@hoteles_bp.route('/buscar', methods=['GET'])
def buscar():
    destino = request.args.get('destino')
    hoteles = Agente5Sim.buscar_hoteles(destino)
    return jsonify({
        "status": "success",
        "count": len(hoteles),
        "data": hoteles
    })

@hoteles_bp.route('/reserva', methods=['POST'])
def reserva():
    datos = request.json
    return jsonify({
        "status": "success",
        "message": "Reserva de hotel iniciada",
        "reserva_id": f"HT-RES-67890",
        "datos": datos
    })
