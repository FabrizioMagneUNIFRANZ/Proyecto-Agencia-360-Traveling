from app import db
from datetime import datetime

class Ciudad(db.Model):
    __tablename__ = 'CIUDAD'
    id_ciudad = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_ciudad = db.Column(db.String(100), nullable=False, unique=True)

class Cliente(db.Model):
    __tablename__ = 'CLIENTE'
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('USUARIO.id_usuario'), nullable=False)
    ci = db.Column(db.String(20), nullable=False, unique=True)
    primer_nombre = db.Column(db.String(50), name='1er_nombre', nullable=False)
    segundo_nombre = db.Column(db.String(50), name='2do_nombre')
    apellido_paterno = db.Column(db.String(50), nullable=False)
    apellido_materno = db.Column(db.String(50))
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(100))

class Empleado(db.Model):
    __tablename__ = 'EMPLEADO'
    id_empleado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('USUARIO.id_usuario'), nullable=False)
    ci = db.Column(db.String(20), nullable=False, unique=True)
    primer_nombre = db.Column(db.String(50), name='1er_nombre', nullable=False)
    segundo_nombre = db.Column(db.String(50), name='2do_nombre')
    apellido_paterno = db.Column(db.String(50), nullable=False)
    apellido_materno = db.Column(db.String(50))
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    telefono = db.Column(db.String(20))

class Hotel(db.Model):
    __tablename__ = 'HOTEL'
    id_hotel = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_ciudad = db.Column(db.Integer, db.ForeignKey('CIUDAD.id_ciudad'), nullable=False)
    nombre_hotel = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(150))
    telefono_hotel = db.Column(db.String(20))

class ActividadTuristica(db.Model):
    __tablename__ = 'ACTIVIDAD_TURISTICA'
    id_actividad = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_ciudad = db.Column(db.Integer, db.ForeignKey('CIUDAD.id_ciudad'), nullable=False)
    nombre_actividad = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    lugar = db.Column(db.String(100))
    fecha_hora = db.Column(db.DateTime, nullable=False)
    cupo = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)

class PaqueteTuristico(db.Model):
    __tablename__ = 'PAQUETE_TURISTICO'
    id_paquete_turistico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('CLIENTE.id_cliente'), nullable=False)
    id_empleado = db.Column(db.Integer, db.ForeignKey('EMPLEADO.id_empleado'), nullable=True)
    nombre_paquete = db.Column(db.String(100))
    numero_personas = db.Column(db.Integer, default=1)
    fecha_inicial = db.Column(db.Date, nullable=False)
    fecha_final = db.Column(db.Date, nullable=False)
    precio_total = db.Column(db.Numeric(10, 2), default=0.00)
    estado = db.Column(db.Enum('borrador', 'cotizacion', 'confirmado', 'cancelado'), default='borrador')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class ReservaVuelo(db.Model):
    __tablename__ = 'RESERVA_VUELO'
    id_reserva_vuelo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_vuelo = db.Column(db.Integer, nullable=False) 
    id_paquete_turistico = db.Column(db.Integer, db.ForeignKey('PAQUETE_TURISTICO.id_paquete_turistico'), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('CLIENTE.id_cliente'), nullable=False)
    fecha_reserva = db.Column(db.Date, default=datetime.utcnow().date)
    numero_pasajeros = db.Column(db.Integer, nullable=False)
    precio_vendido = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.Enum('pendiente_pago', 'realizado', 'cancelado'), default='pendiente_pago')

class ReservaHotel(db.Model):
    __tablename__ = 'RESERVA_HOTEL'
    id_reserva_hotel = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('CLIENTE.id_cliente'), nullable=False)
    id_hotel = db.Column(db.Integer, nullable=False) 
    id_paquete_turistico = db.Column(db.Integer, db.ForeignKey('PAQUETE_TURISTICO.id_paquete_turistico'), nullable=False)
    numero_personas = db.Column(db.Integer, nullable=False)
    tipo_habitacion = db.Column(db.String(50))
    numero_noches = db.Column(db.Integer)
    fecha_reserva = db.Column(db.Date, default=datetime.utcnow().date)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.Enum('pendiente_pago', 'realizado', 'cancelado'), default='pendiente_pago')

class ReservaTraslado(db.Model):
    __tablename__ = 'RESERVA_TRASLADO'
    id_reserva_traslado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('CLIENTE.id_cliente'), nullable=False)
    id_transporte = db.Column(db.Integer, nullable=False) 
    id_paquete_turistico = db.Column(db.Integer, db.ForeignKey('PAQUETE_TURISTICO.id_paquete_turistico'), nullable=False)
    fecha_reserva = db.Column(db.Date, default=datetime.utcnow().date)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    numero_personas = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.Enum('pendiente_pago', 'realizado', 'cancelado'), default='pendiente_pago')

class ReservaSeguro(db.Model):
    __tablename__ = 'RESERVA_SEGURO'
    id_reserva_seguro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('CLIENTE.id_cliente'), nullable=False)
    id_seguro = db.Column(db.Integer, nullable=False) 
    id_paquete_turistico = db.Column(db.Integer, db.ForeignKey('PAQUETE_TURISTICO.id_paquete_turistico'), nullable=False)
    fecha_reserva = db.Column(db.Date, default=datetime.utcnow().date)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.Enum('pendiente_pago', 'realizado', 'cancelado'), default='pendiente_pago')

class ReservaActividad(db.Model):
    __tablename__ = 'RESERVA_ACTIVIDAD'
    id_reserva_actividad = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('CLIENTE.id_cliente'), nullable=False)
    id_actividad = db.Column(db.Integer, nullable=False) 
    id_paquete_turistico = db.Column(db.Integer, db.ForeignKey('PAQUETE_TURISTICO.id_paquete_turistico'), nullable=False)
    numero_personas = db.Column(db.Integer, nullable=False)
    fecha_reserva = db.Column(db.Date, default=datetime.utcnow().date)
    estado = db.Column(db.Enum('pendiente_pago', 'realizado', 'cancelado'), default='pendiente_pago')

class ReservaLog(db.Model):
    __tablename__ = 'RESERVA_LOG'
    id_log = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_cliente = db.Column(db.String(100))
    detalles_servicios = db.Column(db.Text)
    monto_total = db.Column(db.Float)
    fecha_reserva = db.Column(db.DateTime, default=datetime.utcnow)
