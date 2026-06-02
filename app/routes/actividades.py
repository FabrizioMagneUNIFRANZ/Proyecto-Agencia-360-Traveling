from flask import Blueprint, jsonify, request
from app.services.agente5_sim import Agente5Sim

actividades_bp = Blueprint('actividades', __name__)

@actividades_bp.route('/buscar', methods=['GET'])
def buscar():
    destino = request.args.get('destino')
    actividades = Agente5Sim.buscar_actividades(destino)
    return jsonify({
        "status": "success",
        "count": len(actividades),
        "data": actividades
    })
