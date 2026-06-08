from app import create_app, db
from app.models.usuario import Usuario
from app.models.reserva import Empleado
from datetime import datetime

def create_admin():
    app = create_app()
    with app.app_context():
        # 0. Asegurar que la columna contraseña sea suficientemente larga
        try:
            db.session.execute(db.text("ALTER TABLE USUARIO MODIFY contraseña VARCHAR(255)"))
            db.session.commit()
            print("Columna 'contraseña' actualizada a 255 caracteres.")
        except Exception as e:
            print(f"Aviso al actualizar columna: {e}")

        # Datos del administrador
        correo = "admin@gmail.com"
        password = "123"
        rol = "administrador"
        
        # Verificar si ya existe y eliminarlo para asegurar el nuevo hash
        user_exists = Usuario.query.filter_by(correo_usuario=correo).first()
        if user_exists:
            # Eliminar perfiles asociados primero
            Empleado.query.filter_by(id_usuario=user_exists.id_usuario).delete()
            db.session.delete(user_exists)
            db.session.commit()
            print(f"Usuario {correo} anterior eliminado para actualización.")

        try:
            # 1. Crear Usuario
            nuevo_usuario = Usuario(
                correo_usuario=correo,
                rol=rol,
                fecha_registro=datetime.utcnow().date(),
                estado='activo'
            )
            nuevo_usuario.set_password(password)
            db.session.add(nuevo_usuario)
            db.session.flush() # Para obtener el ID

            # 2. Crear Perfil de Empleado para el Administrador
            nuevo_empleado = Empleado(
                id_usuario=nuevo_usuario.id_usuario,
                ci="0000000",
                primer_nombre="Admin",
                apellido_paterno="Principal",
                fecha_nacimiento=datetime(1990, 1, 1).date(),
                telefono="00000000"
            )
            db.session.add(nuevo_empleado)
            
            db.session.commit()
            print(f"Administrador {correo} creado exitosamente.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear el administrador: {e}")

if __name__ == "__main__":
    create_admin()
