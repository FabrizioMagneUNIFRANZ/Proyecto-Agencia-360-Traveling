from app import create_app
import os
from dotenv import load_dotenv

# Cargar variables de entorno adicionales
load_dotenv()

# Crear la instancia de la aplicación
app = create_app()

if __name__ == '__main__':
    # Configurar puerto, por defecto 5000 para Flask
    port = int(os.getenv('PORT', 5000))
    # Iniciar el servidor de desarrollo en modo debug
    app.run(host='0.0.0.0', port=port, debug=True)
