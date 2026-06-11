from flask import Blueprint, jsonify, request
from app import db
from app.models.reserva import (
    Cliente, PaqueteTuristico, ReservaVuelo, ReservaHotel, 
    ReservaTraslado, ReservaSeguro, ReservaActividad, ReservaLog
)
from app.models.usuario import Usuario
from datetime import datetime, date
import json

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/confirmar', methods=['POST'])
def confirmar_reserva():
    try:
        data = request.json
        
        # 1. Buscar o crear el Cliente (Simplificado: buscamos por CI)
        cliente = Cliente.query.filter_by(ci=data['doc_num']).first()
        print(f"DEBUG data recibida: {data}")
        if not cliente:
            # Para este flujo, si no existe, creamos un Usuario temporal o usamos uno genérico
            # En un flujo real, el usuario ya debería estar logueado o registrarse
            usuario_generico = Usuario.query.filter_by(correo_usuario=data['email']).first()
            if not usuario_generico:
                # Crear un usuario base si no existe ninguno
                print(f"DEBUG creando usuario con email: {data['email']}")
                usuario_generico = Usuario(
                    rol='cliente',
                    correo_usuario=data['email'],
                    # contraseña='password123', # Hash en producción
                    fecha_registro=date.today()
                )
                usuario_generico.set_password(data.get('password', 'password123'))
                db.session.add(usuario_generico)
                db.session.flush()

            cliente = Cliente(
                id_usuario=usuario_generico.id_usuario,
                ci=data['doc_num'],
                primer_nombre=data['name'],
                apellido_paterno=data['lastname'],
                fecha_nacimiento=date(1990, 1, 1), # Valor por defecto o pedir en checkout
                telefono=data['phone'],
                correo=data['email']
            )
            db.session.add(cliente)
            db.session.flush()

        # 2. Crear el Paquete Turístico (Contenedor Maestro)
        nuevo_paquete = PaqueteTuristico(
            id_cliente=cliente.id_cliente,
            nombre_paquete=f"Viaje de {data['name']}",
            fecha_inicial=date.today(),
            fecha_final=date.today(), # Actualizar según servicios
            precio_total=float(data['total']),
            estado='confirmado'
        )
        db.session.add(nuevo_paquete)
        db.session.flush()

        # 3. Registrar cada servicio del carrito en su tabla correspondiente
        cart = data.get('cart', [])
        for item in cart:
            tipo = item.get('type')
            precio = float(item.get('price', 0))
            
            if tipo == 'vuelos':
                res = ReservaVuelo(
                    id_vuelo=0, # El ID real vendría del simulador/API
                    id_paquete_turistico=nuevo_paquete.id_paquete_turistico,
                    id_cliente=cliente.id_cliente,
                    numero_pasajeros=1,
                    precio_vendido=precio
                )
                db.session.add(res)
            
            elif tipo == 'hoteles':
                res = ReservaHotel(
                    id_cliente=cliente.id_cliente,
                    id_hotel=0,
                    id_paquete_turistico=nuevo_paquete.id_paquete_turistico,
                    numero_personas=1,
                    precio=precio
                )
                db.session.add(res)
            
            elif tipo == 'transporte':
                res = ReservaTraslado(
                    id_cliente=cliente.id_cliente,
                    id_transporte=0,
                    id_paquete_turistico=nuevo_paquete.id_paquete_turistico,
                    fecha_hora=datetime.now(),
                    numero_personas=1,
                    precio=precio
                )
                db.session.add(res)
            
            elif tipo == 'seguros':
                res = ReservaSeguro(
                    id_cliente=cliente.id_cliente,
                    id_seguro=0,
                    id_paquete_turistico=nuevo_paquete.id_paquete_turistico,
                    fecha_inicio=date.today(),
                    fecha_fin=date.today(),
                    precio=precio
                )
                db.session.add(res)
            
            elif tipo == 'actividades':
                res = ReservaActividad(
                    id_cliente=cliente.id_cliente,
                    id_actividad=0,
                    id_paquete_turistico=nuevo_paquete.id_paquete_turistico,
                    numero_personas=1
                )
                db.session.add(res)

        # 4. Guardar Log General
        log = ReservaLog(
            nombre_cliente=f"{data['name']} {data['lastname']}",
            detalles_servicios=json.dumps(cart),
            monto_total=float(data['total'])
        )
        db.session.add(log)
        
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Reserva guardada en la base de datos normalizada",
            "id_reserva": nuevo_paquete.id_paquete_turistico
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error en confirmar_reserva: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
