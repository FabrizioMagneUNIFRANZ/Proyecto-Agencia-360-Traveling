from flask import Blueprint, jsonify, request
from app.services.agente5_sim import Agente5Sim

seguros_bp = Blueprint('seguros', __name__)

@seguros_bp.route('/buscar', methods=['GET'])
def buscar():
    seguros = Agente5Sim.buscar_seguros()
    return jsonify({
        "status": "success",
        "count": len(seguros),
        "data": seguros
    })
