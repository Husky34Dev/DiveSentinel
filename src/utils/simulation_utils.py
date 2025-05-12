# src/utils/simulation_utils.py
import random
from src.config import (
    SURFACE_PRESSURE_BAR,
    DEPTH_PRESSURE_FACTOR,
    SURFACE_AIR_CONSUMPTION_LPM,
    WORKLOAD_FACTOR,
    GAS_FACTORS,
    EXPERIENCE_FACTORS,
    MAR_CONDITION_FACTORS,
    TANK_VOLUME_L,
    TANK_VOLUMES_L,
    CONSUMPTION_NOISE_STD,
    NDL_TABLE,
    DECO_STOPS,
)

def pressure_at_depth(depth_m: float) -> float:
    """Presión absoluta (bar) a profundidad depth_m."""
    return SURFACE_PRESSURE_BAR + (depth_m / DEPTH_PRESSURE_FACTOR)


def ndl_limit(depth_m: float) -> float:
    """Devuelve el NDL (min) más cercano por debajo de depth_m."""
    depths = sorted(NDL_TABLE.keys())
    for d in depths:
        if depth_m <= d:
            return NDL_TABLE[d]
    return NDL_TABLE[depths[-1]]


def required_deco_stops(depth_m: float) -> list[tuple[int,int]]:
    """
    Si la inmersión rompe el NDL a depth_m, devuelve la lista de paradas
    (profundidad_m, tiempo_min) a realizar.
    """
    return DECO_STOPS.get(int(depth_m), [])


def gas_consumption(
    depth_m: float,
    phase: str,
    tipo_gas: str,
    nivel_exp: str,
    condiciones_mar: str,
    tank_volume: float = TANK_VOLUME_L,
) -> float:
    """
    Retorna consumo en BAR/min, con opción de especificar volumen de tanque:
     - ajusta por presión ambiente y phase
     - aplica factor de gas, experiencia y mar
     - añade ruido gaussiano proporcional

    Parámetros:
      depth_m       -- profundidad actual en metros
      phase         -- una de: 'descenso','fondo','ascenso','deco_stop','safety_stop'
      tipo_gas      -- 'Aire','Nitrox','Trimix'
      nivel_exp     -- 'Principiante','Intermedio','Avanzado'
      condiciones_mar -- 'Calmado','Moderado','Agitado'
      tank_volume   -- volumen del cilindro en litros (por defecto TANK_VOLUME_L)

    Devuelve:
      Consumo en bar/min (float)
    """
    # 1) consumo base en L/min a esa profundidad y fase
    p = pressure_at_depth(depth_m)
    lpm = SURFACE_AIR_CONSUMPTION_LPM * p * WORKLOAD_FACTOR.get(phase, 1.0)

    # 2) factores de gas, experiencia y condiciones
    factor_gas = GAS_FACTORS.get(tipo_gas, 1.0)
    factor_exp = EXPERIENCE_FACTORS.get(nivel_exp, 1.0)
    factor_mar = MAR_CONDITION_FACTORS.get(condiciones_mar, 1.0)
    lpm *= (factor_gas * factor_exp * factor_mar)

    # 3) convertimos a bar/min usando el volumen de tanque
    bar_per_min = lpm / tank_volume

    # 4) añadimos ruido aleatorio gaussiano
    ruido = random.gauss(0, CONSUMPTION_NOISE_STD * bar_per_min)
    bar_per_min_noisy = max(bar_per_min + ruido, 0)

    return bar_per_min_noisy