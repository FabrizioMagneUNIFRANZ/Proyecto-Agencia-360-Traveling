from flask import Blueprint, jsonify, request
from app.services.agente5_sim import Agente5Sim

transporte_bp = Blueprint('transporte', __name__)

@transporte_bp.route('/buscar', methods=['GET'])
def buscar():
    destino = request.args.get('destino')
    transportes = Agente5Sim.buscar_transporte(destino)
    return jsonify({
        "status": "success",
        "count": len(transportes),
        "data": transportes
    })
