from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'USUARIO'
    
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rol = db.Column(db.Enum('cliente', 'agente', 'administrador'), nullable=False)
    correo_usuario = db.Column(db.String(100), unique=True, nullable=False)
    # Mapeamos 'contraseña' usando el argumento 'name' por el caracter especial 'ñ'
    contraseña = db.Column(db.String(255), name='contraseña', nullable=False)
    fecha_registro = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    estado = db.Column(db.Enum('activo', 'inactivo'), nullable=False, default='activo')
    
    def set_password(self, password):
        self.contraseña = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.contraseña, password)
    
    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "rol": self.rol,
            "correo_usuario": self.correo_usuario,
            "fecha_registro": str(self.fecha_registro) if self.fecha_registro else None,
            "estado": self.estado
        }
