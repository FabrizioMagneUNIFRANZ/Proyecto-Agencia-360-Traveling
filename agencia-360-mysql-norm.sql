-- ============================================================
-- MODELO FISICO  |  Motor: MySQL / MariaDB
-- Proyecto: Sistema Web para la administración y gestión de vuelos y paquetes turísticos de la empresa “360° Traveling”
-- Version:  1.6
-- ============================================================

-- =========================
-- USUARIO
-- =========================
CREATE TABLE USUARIO (
    id_usuario INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    rol ENUM('cliente', 'agente', 'administrador') NOT NULL,
    correo_usuario VARCHAR(100) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    fecha_registro DATE NOT NULL,
    estado ENUM('activo','inactivo') NOT NULL DEFAULT 'activo'
);

-- =========================
-- CLIENTE
-- =========================
CREATE TABLE CLIENTE (
    id_cliente INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNSIGNED NOT NULL,
    ci VARCHAR(20) NOT NULL UNIQUE,
    `1er_nombre` VARCHAR(50) NOT NULL,
    `2do_nombre` VARCHAR(50),
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50),
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100),
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario)
);

-- =========================
-- EMPLEADO
-- =========================
CREATE TABLE EMPLEADO (
    id_empleado INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNSIGNED NOT NULL,
    ci VARCHAR(20) NOT NULL UNIQUE,
    `1er_nombre` VARCHAR(50) NOT NULL,
    `2do_nombre` VARCHAR(50),
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50),
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(20),
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario)
);

-- =========================
-- CIUDAD
-- =========================
CREATE TABLE CIUDAD (
    id_ciudad INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_ciudad VARCHAR(100) NOT NULL UNIQUE
);

-- =========================
-- HOTEL
-- =========================
CREATE TABLE HOTEL (
    id_hotel INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_ciudad INT UNSIGNED NOT NULL,
    nombre_hotel VARCHAR(100) NOT NULL,
    direccion VARCHAR(150),
    telefono_hotel VARCHAR(20),
    FOREIGN KEY (id_ciudad) REFERENCES CIUDAD(id_ciudad)
);

-- =========================
-- AEROLINEA
-- =========================
CREATE TABLE AEROLINEA (
    id_aerolinea INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_aerolinea VARCHAR(100) NOT NULL UNIQUE,
    direccion_central VARCHAR(150),
    telefono_aerolinea VARCHAR(20)
);

-- =========================
-- OPERADORA_TRASLADO
-- =========================
CREATE TABLE OPERADORA_TRASLADO (
    id_operadora INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_operadora VARCHAR(100) NOT NULL UNIQUE,
    telefono_operadora VARCHAR(20),
    direccion VARCHAR(150)
);

-- ============================================================
-- NUEVO: COMPAÑIA_SEGURO (Para soporte de Seguro de Viaje)
-- ============================================================
CREATE TABLE COMPAÑIA_SEGURO (
    id_compañia INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_compañia VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    direccion VARCHAR(150)
);

-- ============================================================
-- NUEVO: SEGURO_VIAJE (Planes de Seguro)
-- ============================================================
CREATE TABLE SEGURO_VIAJE (
    id_seguro INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_compañia INT UNSIGNED NOT NULL,
    nombre_plan VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio_por_dia DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_compañia) REFERENCES COMPAÑIA_SEGURO(id_compañia)
);

-- ============================================================
-- NUEVO: TRANSPORTE_TERRESTRE (Catálogo Maestro de Servicios de Transporte)
-- ============================================================
CREATE TABLE TRANSPORTE_TERRESTRE (
    id_transporte INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_operadora INT UNSIGNED NOT NULL,
    tipo_transporte ENUM('shuttle_aeropuerto', 'autobus_interurbano', 'servicio_privado', 'alquiler_auto') NOT NULL,
    id_origen INT UNSIGNED NOT NULL,
    id_destino INT UNSIGNED NOT NULL,
    descripcion VARCHAR(255),
    capacidad INT UNSIGNED NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_operadora) REFERENCES OPERADORA_TRASLADO(id_operadora),
    FOREIGN KEY (id_origen) REFERENCES CIUDAD(id_ciudad),
    FOREIGN KEY (id_destino) REFERENCES CIUDAD(id_ciudad)
);

-- ============================================================
-- MEJORADO: PAQUETE_TURISTICO (Contenedor Maestro de Reservas de Viaje)
-- ============================================================
CREATE TABLE PAQUETE_TURISTICO (
    id_paquete_turistico INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT UNSIGNED NOT NULL,
    id_empleado INT UNSIGNED DEFAULT NULL, -- Agente que gestionó la reserva (opcional)
    nombre_paquete VARCHAR(100) DEFAULT NULL,
    numero_personas INT UNSIGNED NOT NULL DEFAULT 1,
    fecha_inicial DATE NOT NULL,
    fecha_final DATE NOT NULL,
    precio_total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    estado ENUM('borrador', 'cotizacion', 'confirmado', 'cancelado') NOT NULL DEFAULT 'borrador',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente),
    FOREIGN KEY (id_empleado) REFERENCES EMPLEADO(id_empleado)
);

-- =========================
-- VUELO
-- =========================
CREATE TABLE VUELO (
    id_vuelo INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_aerolinea INT UNSIGNED NOT NULL,
    id_origen INT UNSIGNED NOT NULL,
    id_destino INT UNSIGNED NOT NULL,
    fecha_hora_salida DATETIME NOT NULL,
    fecha_hora_llegada DATETIME NOT NULL,
    escalas INT UNSIGNED DEFAULT 0,
    capacidad INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_aerolinea) REFERENCES AEROLINEA(id_aerolinea),
    FOREIGN KEY (id_origen) REFERENCES CIUDAD(id_ciudad),
    FOREIGN KEY (id_destino) REFERENCES CIUDAD(id_ciudad)
);

-- =========================
-- RESERVA_VUELO
-- =========================
CREATE TABLE RESERVA_VUELO (
    id_reserva_vuelo INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_vuelo INT UNSIGNED NOT NULL,
    id_paquete_turistico INT UNSIGNED NOT NULL,
    id_cliente INT UNSIGNED NOT NULL,
    fecha_reserva DATE NOT NULL,
    numero_pasajeros INT UNSIGNED NOT NULL,
    precio_vendido DECIMAL(10,2) NOT NULL,
    estado ENUM('pendiente_pago','realizado','cancelado') NOT NULL DEFAULT 'pendiente_pago',
    FOREIGN KEY (id_vuelo) REFERENCES VUELO(id_vuelo),
    FOREIGN KEY (id_paquete_turistico) REFERENCES PAQUETE_TURISTICO(id_paquete_turistico),
    FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente)
);

-- =========================
-- BOLETO
-- =========================
CREATE TABLE BOLETO (
    id_boleto INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_reserva_vuelo INT UNSIGNED NOT NULL,
    id_cliente INT UNSIGNED NOT NULL,
    numero_boleto VARCHAR(20) NOT NULL UNIQUE,
    clase ENUM('economica','ejecutiva','primera') NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    estado ENUM('pendiente_pago','realizado','cancelado') NOT NULL DEFAULT 'pendiente_pago',
    FOREIGN KEY (id_reserva_vuelo) REFERENCES RESERVA_VUELO(id_reserva_vuelo),
    FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente)
);

-- =========================
-- ESCALA (opcional)
-- =========================
CREATE TABLE ESCALA (
    id_escala INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_vuelo INT UNSIGNED NOT NULL,
    id_ciudad INT UNSIGNED NOT NULL,
    orden INT UNSIGNED NOT NULL,
    hora_llegada DATETIME,
    hora_salida DATETIME,
    FOREIGN KEY (id_vuelo) REFERENCES VUELO(id_vuelo),
    FOREIGN KEY (id_ciudad) REFERENCES CIUDAD(id_ciudad)
);

-- =========================
-- RESERVA_HOTEL
-- =========================
CREATE TABLE RESERVA_HOTEL (
    id_reserva_hotel INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT UNSIGNED NOT NULL,
    id_hotel INT UNSIGNED NOT NULL,
    id_paquete_turistico INT UNSIGNED NOT NULL,
    numero_personas INT UNSIGNED NOT NULL,
    tipo_habitacion VARCHAR(50),
    numero_dias INT UNSIGNED,
    numero_noches INT UNSIGNED,
    fecha_reserva DATE NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    estado ENUM('pendiente_pago','realizado','cancelado') NOT NULL DEFAULT 'pendiente_pago',
    FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente),
    FOREIGN KEY (id_hotel) REFERENCES HOTEL(id_hotel),
    FOREIGN KEY (id_paquete_turistico) REFERENCES PAQUETE_TURISTICO(id_paquete_turistico)
);

-- ============================================================
-- MEJORADO: RESERVA_TRASLADO (Vinculado a TRANSPORTE_TERRESTRE)
-- ============================================================
CREATE TABLE RESERVA_TRASLADO (
    id_reserva_traslado INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT UNSIGNED NOT NULL,
    id_transporte INT UNSIGNED NOT NULL,
    id_paquete_turistico INT UNSIGNED NOT NULL,
    fecha_reserva DATE NOT NULL,
    fecha_hora DATETIME NOT NULL,
    numero_personas INT UNSIGNED NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    estado ENUM('pendiente_pago','realizado','cancelado') NOT NULL DEFAULT 'pendiente_pago',
    FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente),
    FOREIGN KEY (id_transporte) REFERENCES TRANSPORTE_TERRESTRE(id_transporte),
    FOREIGN KEY (id_paquete_turistico) REFERENCES PAQUETE_TURISTICO(id_paquete_turistico)
);

-- ============================================================
-- NUEVO: RESERVA_SEGURO (Seguro de viaje opcional del paquete)
-- ============================================================
CREATE TABLE RESERVA_SEGURO (
    id_reserva_seguro INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT UNSIGNED NOT NULL,
    id_seguro INT UNSIGNED NOT NULL,
    id_paquete_turistico INT UNSIGNED NOT NULL,
    fecha_reserva DATE NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    estado ENUM('pendiente_pago','realizado','cancelado') NOT NULL DEFAULT 'pendiente_pago',
    FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente),
    FOREIGN KEY (id_seguro) REFERENCES SEGURO_VIAJE(id_seguro),
    FOREIGN KEY (id_paquete_turistico) REFERENCES PAQUETE_TURISTICO(id_paquete_turistico)
);

-- =========================
-- ACTIVIDAD_TURISTICA
-- =========================
CREATE TABLE ACTIVIDAD_TURISTICA (
    id_actividad INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_ciudad INT UNSIGNED NOT NULL,
    nombre_actividad VARCHAR(100) NOT NULL,
    descripcion TEXT,
    lugar VARCHAR(100),
    fecha_hora DATETIME NOT NULL,
    cupo INT UNSIGNED NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_ciudad) REFERENCES CIUDAD(id_ciudad)
);

-- ============================================================
-- CORREGIDO: RESERVA_ACTIVIDAD (Cierre correcto de llaves y sintaxis)
-- ============================================================
CREATE TABLE RESERVA_ACTIVIDAD (
    id_reserva_actividad INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT UNSIGNED NOT NULL,
    id_actividad INT UNSIGNED NOT NULL,
    id_paquete_turistico INT UNSIGNED NOT NULL,
    numero_personas INT UNSIGNED NOT NULL,
    fecha_reserva DATE NOT NULL,
    estado ENUM('pendiente_pago','realizado','cancelado') NOT NULL DEFAULT 'pendiente_pago',
    FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente),
    FOREIGN KEY (id_actividad) REFERENCES ACTIVIDAD_TURISTICA(id_actividad),
    FOREIGN KEY (id_paquete_turistico) REFERENCES PAQUETE_TURISTICO(id_paquete_turistico)
);
