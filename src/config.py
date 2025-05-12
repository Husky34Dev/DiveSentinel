import os

# --- API ---
API_URL = os.getenv("API_URL", "http://localhost:5001")
API_TIMEOUT = 5  # segundos para timeout de requests
# Path al pipeline entrenado (exportado por scripts/train_model.py)
MODEL_PATH = os.getenv("MODEL_PATH", "src/models/pipeline_gbc.joblib")

# --- SIMULACIÓN BÁSICA ---
RANGO_TEMPERATURA     = (10.0, 25.0)    # en °C
NIVELES_EXPERIENCIA   = ["Principiante", "Intermedio", "Avanzado"]
CONDICIONES_MAR       = ["Calmado", "Moderado", "Agitado"]
TIPOS_GAS             = ["Aire", "Nitrox", "Trimix"]

# Ahora muestreamos profundidades de 5 a 60 m (en lugar de [15,20,30,40])
PROFUNDIDADES_MAX     = list(range(5, 61))  # en metros

# Lista de volúmenes de cilindro para variar
TANK_VOLUMES_L        = [10.0, 12.0, 15.0, 18.0]  # en litros

# (Se mantiene para compatibilidad con partes de código que usan un único valor)
TANK_VOLUME_L         = 12.0

# Semilla para reproducibilidad
SEED = 42

# --- PARADAS DE SEGURIDAD SIMPLIFICADAS ---
PARADA_PROF_UMBRAL   = 30  # m: profundidad a partir de la cual se recomienda
PARADA_TIEMPO_UMBRAL = 20  # min: tiempo en fondo tras el cual se recomienda

# --- MODELO DE PRESIÓN Y CONSUMO REALISTA ---
SURFACE_PRESSURE_BAR        = 1.0     # bar al nivel de superficie
DEPTH_PRESSURE_FACTOR       = 10.0    # +1 bar cada 10 m

# Tasa de consumo base a superficie (L/min)
SURFACE_AIR_CONSUMPTION_LPM = 20

# Factores de trabajo según fase de la inmersión
WORKLOAD_FACTOR = {
    "descenso":    1.3,
    "fondo":       1.5,
    "ascenso":     1.2,
    "deco_stop":   1.2,
    "safety_stop": 1.1,
}

# Velocidades recomendadas (m/min)
DESCENT_RATE_M_PER_MIN = 18
ASCENT_RATE_M_PER_MIN  = 9

# --- NO-DECOMPRESSION LIMITS (NDL) simplificados ---
# profundidad (m) → NDL (min)
NDL_TABLE = {
    10: 200,
    20:  50,
    30:  25,
    40:  15,
    50:  10,
}

# Paradas de descompresión obligatorias si se excede NDL
# { profundidad_más_cercana: [(prof_parada_m, tiempo_min), ...] }
DECO_STOPS = {
    40: [(3, 5)],
    50: [(6, 3), (3, 5)],
}

# Factores por tipo de gas
GAS_FACTORS = {
    "Aire":   1.00,
    "Nitrox": 0.90,
    "Trimix": 0.85,
}

# Factores por nivel de experiencia
EXPERIENCE_FACTORS = {
    "Principiante": 1.15,
    "Intermedio":   1.00,
    "Avanzado":     0.90,
}

# Factores por condiciones de mar
MAR_CONDITION_FACTORS = {
    "Calmado":   1.00,
    "Moderado":  1.10,
    "Agitado":   1.25,
}

# Desviación estándar para ruido en el consumo (± en proporción)
CONSUMPTION_NOISE_STD = 0.05  # 5%

# --- SAFETY STOP GLOBAL ---
SAFETY_STOP_DEPTH_THRESHOLD_M = 10   # si buceo fue >10 m
SAFETY_STOP_AT_DEPTH_M        = 5    # a 5 m
SAFETY_STOP_DURATION_MIN      = 3    # durante 3 min

# Reserva mínima de aire para inmersión segura (bar)
RESERVE_AIR_BAR = 30
