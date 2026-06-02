from flask import Flask, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

# Instanciar el ORM SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Inicializar la aplicación Flask
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Habilitar CORS
    CORS(app)
    
    # Inicializar la base de datos con la configuración de la app
    try:
        db.init_app(app)
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
    
    # Importar y registrar Blueprints (Rutas Modulares)
    from app.routes.auth import auth_bp
    from app.routes.vuelos import vuelos_bp
    from app.routes.paquetes import paquetes_bp
    from app.routes.hoteles import hoteles_bp
    from app.routes.transporte import transporte_bp
    from app.routes.seguros import seguros_bp
    from app.routes.actividades import actividades_bp
    from app.routes.reservas import reservas_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(vuelos_bp, url_prefix='/api/vuelos')
    app.register_blueprint(paquetes_bp, url_prefix='/api/paquetes')
    app.register_blueprint(hoteles_bp, url_prefix='/api/hoteles')
    app.register_blueprint(transporte_bp, url_prefix='/api/transporte')
    app.register_blueprint(seguros_bp, url_prefix='/api/seguros')
    app.register_blueprint(actividades_bp, url_prefix='/api/actividades')
    app.register_blueprint(reservas_bp, url_prefix='/api/reservas')
    
    # Rutas de prueba base
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/results')
    def results():
        return render_template('results.html')

    @app.route('/checkout')
    def checkout():
        return render_template('checkout.html')

    @app.route('/payment')
    def payment():
        return render_template('payment.html')

    return app
