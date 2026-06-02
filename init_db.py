import pymysql
from app import create_app, db
from app.config import Config
from datetime import datetime
from app.models.usuario import Usuario
from app.models.reserva import (
    Ciudad, Cliente, Empleado, Hotel, ActividadTuristica, PaqueteTuristico, ReservaVuelo, 
    ReservaHotel, ReservaTraslado, ReservaSeguro, ReservaActividad, ReservaLog
)

def initialize():
    # 1. Crear la base de datos si no existe
    try:
        connection = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASS,
            port=int(Config.DB_PORT)
        )
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
        connection.close()
        print(f"Base de datos '{Config.DB_NAME}' verificada/creada.")
    except Exception as e:
        print(f"Error al crear la base de datos: {e}")
        return

    # 2. Crear las tablas usando SQLAlchemy
    app = create_app()
    with app.app_context():
        # db.drop_all() # Descomenta si necesitas limpiar todo
        db.create_all()
        print("Tablas creadas correctamente en MySQL siguiendo el modelo normalizado.")

        # 3. Poblar Ciudades Capitales de Bolivia
        ciudades_capitales = [
            "Santa Cruz de la Sierra", "La Paz", "Cochabamba", "Sucre", 
            "Potosí", "Oruro", "Tarija", "Trinidad", "Cobija"
        ]
        
        for nombre in ciudades_capitales:
            if not Ciudad.query.filter_by(nombre_ciudad=nombre).first():
                nueva_ciudad = Ciudad(nombre_ciudad=nombre)
                db.session.add(nueva_ciudad)
        
        db.session.commit()
        print("Ciudades capitales de Bolivia registradas.")

        # 4. Poblar algunos Hoteles y Actividades vinculados
        scz = Ciudad.query.filter_by(nombre_ciudad="Santa Cruz de la Sierra").first()
        lpz = Ciudad.query.filter_by(nombre_ciudad="La Paz").first()
        
        if scz and not Hotel.query.filter_by(id_ciudad=scz.id_ciudad).first():
            db.session.add(Hotel(id_ciudad=scz.id_ciudad, nombre_hotel="Los Tajibos Hotel", direccion="Av. San Martin"))
            db.session.add(ActividadTuristica(id_ciudad=scz.id_ciudad, nombre_actividad="Tour Misiones Jesuíticas", fecha_hora=datetime.now(), cupo=20, precio=150))
        
        if lpz and not Hotel.query.filter_by(id_ciudad=lpz.id_ciudad).first():
            db.session.add(Hotel(id_ciudad=lpz.id_ciudad, nombre_hotel="Hotel Casa Grande", direccion="Calacoto"))
            db.session.add(ActividadTuristica(id_ciudad=lpz.id_ciudad, nombre_actividad="City Tour Teleférico", fecha_hora=datetime.now(), cupo=15, precio=50))

        db.session.commit()
        print("Hoteles y Actividades base vinculados correctamente.")

if __name__ == "__main__":
    initialize()
