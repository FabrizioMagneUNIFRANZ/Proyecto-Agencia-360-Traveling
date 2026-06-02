import random
from datetime import datetime, timedelta

class Agente5Sim:
    """
    Simulador de API Agente5 para generar ofertas de vuelos, hoteles, transporte, seguros y actividades.
    Enfocado en el mercado boliviano.
    """
    
    AEROLINEAS = ["Boliviana de Aviación (BoA)", "EcoJet", "Amaszonas (Nest)"]
    CIUDADES = ["Santa Cruz", "La Paz", "Cochabamba", "Sucre", "Tarija", "Potosí", "Oruro", "Trinidad", "Cobija", "Uyuni"]
    HOTELES = [
        "Hotel Camino Real (Bolivia)", "Los Tajibos a Tribute Portfolio", "Marriott Santa Cruz", 
        "Radisson Plaza La Paz", "Hotel Casa Grande", "Gran Hotel Cochabamba", 
        "Hotel Parador Santa Maria la Real", "Hotel Luna Salada (Uyuni)", "Palacio de Sal",
        "Hotel Gloria (La Paz)", "Hotel Libertador (Sucre)", "Hotel Victoria (Potosí)",
        "Hotel Tarija", "Hotel Trinidad", "Hotel Cobija"
    ]
    TRANSPORTES = ["Transfer Privado Aeropuerto", "SUV 4x4 Uyuni", "Minibús Turístico", "Radio Taxi Seguro"]
    SEGUROS = ["Seguro Viajero Básico", "Seguro Premium Total", "Seguro Cancelación Flexible"]
    ACTIVIDADES = [
        "Tour Salar de Uyuni Full Day", "City Tour La Paz y Teleférico", "Ruta del Vino Tarija", 
        "Visita a las Misiones Jesuíticas", "Caminata por el Tiwanaku", "Tour Gastronómico Cochabamba",
        "Tour Potosí Minas", "City Tour Sucre Histórico", "Tour Pantanal (Puerto Suárez)",
        "Tour Yungas (Coroico)", "Tour Chapare (Cochabamba)"
    ]

    @classmethod
    def buscar_vuelos(cls, origen, destino, fecha_salida):
        vuelos = []
        # Normalizar nombres de ciudades para la simulación
        ciudades_bolivia = [
            "Santa Cruz de la Sierra", "La Paz", "Cochabamba", "Sucre", 
            "Potosí", "Oruro", "Tarija", "Trinidad", "Cobija"
        ]
        
        for _ in range(random.randint(3, 6)):
            aerolinea = random.choice(cls.AEROLINEAS)
            precio = random.randint(450, 1500)
            hora_salida = f"{random.randint(0, 23):02}:{random.randint(0, 59):02}"
            
            vuelos.append({
                "id": f"FL-{random.randint(1000, 9999)}",
                "aerolinea": aerolinea,
                "origen": origen or random.choice(ciudades_bolivia),
                "destino": destino or random.choice(ciudades_bolivia),
                "fecha": fecha_salida or datetime.now().strftime("%Y-%m-%d"),
                "hora": hora_salida,
                "precio": precio,
                "moneda": "USD",
                "tipo": "Vuelo"
            })
        return sorted(vuelos, key=lambda x: x['precio'])

    @classmethod
    def buscar_hoteles(cls, destino):
        hoteles = []
        # Simular vinculación por destino
        # En una app real, esto sería una consulta SQL: Hotel.query.filter_by(ciudad=destino)
        
        # Filtro de hoteles por palabras clave del destino
        hoteles_filtrados = [h for h in cls.HOTELES if (destino and destino.lower() in h.lower())]
        if not hoteles_filtrados: hoteles_filtrados = cls.HOTELES

        for _ in range(min(4, len(hoteles_filtrados))):
            nombre = random.choice(hoteles_filtrados)
            estrellas = random.randint(3, 5)
            precio_noche = random.randint(40, 250)
            
            hoteles.append({
                "id": f"HT-{random.randint(1000, 9999)}",
                "nombre": nombre,
                "destino": destino or "Bolivia",
                "estrellas": estrellas,
                "precio_noche": precio_noche,
                "moneda": "USD",
                "tipo": "Hotel"
            })
        
        if not hoteles:
            hoteles.append({
                "id": "HT-DEF", "nombre": f"Hotel Central {destino or 'Bolivia'}", 
                "destino": destino or "Bolivia", "estrellas": 4, "precio_noche": 85, 
                "moneda": "USD", "tipo": "Hotel"
            })
        return sorted(hoteles, key=lambda x: x['precio_noche'])

    @classmethod
    def buscar_paquetes(cls, destino):
        paquetes = []
        vuelos = cls.buscar_vuelos(None, destino, None)
        hoteles = cls.buscar_hoteles(destino)
        
        if not vuelos or not hoteles:
            return []

        for _ in range(random.randint(2, 5)):
            vuelo = random.choice(vuelos)
            hotel = random.choice(hoteles)
            noches = random.randint(2, 5)
            precio_total = int((vuelo['precio'] + (hotel['precio_noche'] * noches)) * 0.85)
            
            paquetes.append({
                "id": f"PK-{random.randint(1000, 9999)}",
                "nombre": f"Vuelo + Hotel: {destino or hotel['destino']} {noches} Noches",
                "destino": destino or hotel['destino'],
                "noches": noches,
                "vuelo": vuelo,
                "hotel": hotel,
                "precio_total": precio_total,
                "moneda": "USD",
                "tipo": "Paquete"
            })
        return sorted(paquetes, key=lambda x: x['precio_total'])

    @classmethod
    def buscar_transporte(cls, destino):
        transportes = []
        for _ in range(random.randint(2, 4)):
            tipo = random.choice(cls.TRANSPORTES)
            precio = random.randint(15, 80)
            
            transportes.append({
                "id": f"TR-{random.randint(1000, 9999)}",
                "nombre": f"{tipo} en {destino or 'Bolivia'}",
                "destino": destino or "Bolivia",
                "precio": precio,
                "moneda": "USD",
                "tipo": "Transporte"
            })
        return transportes

    @classmethod
    def buscar_seguros(cls):
        seguros = []
        for nombre in cls.SEGUROS:
            precio = random.randint(10, 45)
            seguros.append({
                "id": f"INS-{random.randint(1000, 9999)}",
                "nombre": nombre,
                "precio": precio,
                "moneda": "USD",
                "tipo": "Seguro"
            })
        return seguros

    @classmethod
    def buscar_actividades(cls, destino):
        actividades = []
        # Filtro simple de actividades por destino
        actividades_filtradas = [a for a in cls.ACTIVIDADES if (destino and (destino.lower() in a.lower()))]
        if not actividades_filtradas: actividades_filtradas = cls.ACTIVIDADES

        for _ in range(min(3, len(actividades_filtradas))):
            nombre = random.choice(actividades_filtradas)
            precio = random.randint(25, 120)
            actividades.append({
                "id": f"ACT-{random.randint(1000, 9999)}",
                "nombre": nombre,
                "destino": destino or "Bolivia",
                "precio": precio,
                "moneda": "USD",
                "tipo": "Actividad"
            })
        return actividades
