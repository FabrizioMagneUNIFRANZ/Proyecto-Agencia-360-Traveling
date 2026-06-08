# ✈️ Agencia 360° Traveling - Sistema de Gestión Turística

## 📋 Descripción General
**Agencia 360° Traveling** es una plataforma web integral diseñada para la administración y gestión de servicios turísticos, enfocada principalmente en el mercado boliviano. El sistema permite a los usuarios buscar y reservar vuelos, hoteles, paquetes turísticos, transporte terrestre y seguros de viaje.

El proyecto utiliza una arquitectura moderna con un backend robusto en Python y una base de datos relacional normalizada para garantizar la integridad de la información.

---

## 🚀 Tecnologías Utilizadas

### **Backend**
- **Lenguaje:** Python 3.x
- **Framework:** [Flask](https://flask.palletsprojects.com/)
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) (para la gestión de base de datos)
- **Seguridad:** JWT (JSON Web Tokens) para autenticación y `cryptography` para el manejo de datos sensibles.
- **Entorno:** `python-dotenv` para la gestión de variables de entorno.

### **Base de Datos**
- **Motor:** MySQL / MariaDB
- **Conector:** `PyMySQL`
- **Diseño:** Modelo relacional normalizado (v1.6) con soporte para roles, reservas complejas y auditoría básica.

### **Frontend**
- **Lenguaje:** HTML5, CSS3, JavaScript (Vanilla JS)
- **Estilo:** Diseño responsive personalizado (style.css).

---

## 📂 Estructura del Proyecto

```text
proyecto-360-v2/
├── app/                    # Paquete principal de la aplicación
│   ├── models/             # Modelos de base de datos (SQLAlchemy)
│   ├── routes/             # Blueprints y rutas de la API/Web
│   ├── services/           # Lógica de negocio y simuladores externos
│   ├── static/             # Archivos estáticos (CSS, JS, Imágenes)
│   ├── templates/          # Plantillas HTML (Jinja2)
│   └── config.py           # Configuración de la aplicación
├── app.py                  # Punto de entrada del servidor Flask
├── init_db.py              # Script de inicialización de la base de datos
├── requirements.txt        # Dependencias del proyecto
└── agencia-360-mysql-norm.sql # Esquema SQL normalizado
```

---

## 🛠️ Módulos Principales

1.  **Módulo de Autenticación:** Gestión de usuarios con roles (Cliente, Agente, Administrador).
2.  **Módulo de Vuelos:** Búsqueda de vuelos por origen, destino y fecha. Gestión de aerolíneas y boletos.
3.  **Módulo de Hoteles:** Catálogo de hoteles en diferentes ciudades de Bolivia con reserva por noches.
4.  **Módulo de Paquetes:** Combina vuelos, hoteles y otros servicios en una sola reserva simplificada.
5.  **Módulo de Transporte:** Gestión de traslados (shuttle, privado, alquiler de autos).
6.  **Módulo de Seguros:** Planes de seguro de viaje integrados.
7.  **Agente5 Sim:** Un simulador de API externa que genera ofertas dinámicas de servicios turísticos para pruebas y desarrollo.

---

## 🔧 Configuración e Instalación

### 1. Requisitos Previos
- Python 3.8+
- MySQL Server

### 2. Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### 3. Configuración de Base de Datos
1. Crear una base de datos llamada `agencia_360` en MySQL.
2. Ejecutar el script `agencia-360-mysql-norm.sql` para crear las tablas.
3. Configurar las credenciales en un archivo `.env` o directamente en [config.py](file:///d%3A/Proyecto%20agencia%20-%20git/proyecto-360-v2/app/config.py).

### 4. Ejecución
```bash
python app.py
```
El servidor se iniciará en `http://localhost:5000`.

---

## 👥 Roles de Usuario y Administración

El sistema cuenta con un módulo de administración que gestiona tres niveles de acceso:

- **Clientes:** 
  - Registro de datos personales.
  - Acceso al historial de servicios y reservas realizadas.
- **Agentes de Viaje:** 
  - Dashboard con visualización de registros de vuelos, hoteles, paquetes y otros servicios.
  - Generación de reportes mensuales de gestión y ventas.
- **Administrador:** 
  - Todas las capacidades del Agente.
  - Gestión completa de usuarios (añadir, modificar y eliminar).
  - Supervisión del rendimiento y ventas de cada agente.

---

## 🔐 Autenticación
El sistema incluye un sistema de Login y Registro que permite a los usuarios acceder a sus respectivos paneles según su rol asignado.

---

## 📝 Nota sobre el Desarrollo
Este proyecto incluye un simulador avanzado ([agente5_sim.py](file:///d%3A/Proyecto%20agencia%20-%20git/proyecto-360-v2/app/services/agente5_sim.py)) que permite probar todas las funcionalidades de búsqueda sin necesidad de conectarse a APIs reales de aerolíneas o hoteles, facilitando el desarrollo y la demostración del sistema.
