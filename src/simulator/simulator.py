# src/utils/simulator.py
import random
from src.config import (
    RANGO_TEMPERATURA, NIVELES_EXPERIENCIA, CONDICIONES_MAR,
    TIPOS_GAS, PROFUNDIDADES_MAX, SEED,
    DESCENT_RATE_M_PER_MIN, ASCENT_RATE_M_PER_MIN,
    TANK_VOLUME_L, TANK_VOLUMES_L,
    SURFACE_PRESSURE_BAR, DEPTH_PRESSURE_FACTOR,
    SURFACE_AIR_CONSUMPTION_LPM,
    WORKLOAD_FACTOR,
    GAS_FACTORS, EXPERIENCE_FACTORS, MAR_CONDITION_FACTORS,
    NDL_TABLE, DECO_STOPS,
    SAFETY_STOP_DEPTH_THRESHOLD_M, SAFETY_STOP_AT_DEPTH_M,
    SAFETY_STOP_DURATION_MIN, RESERVE_AIR_BAR
)
from src.utils.simulation_utils import (
    gas_consumption, ndl_limit, required_deco_stops
)

random.seed(SEED)

# Probabilidades de fallo aleatorio
FAIL_DECO_PROB = 0.05         # 5% de olvidar parada deco
FAIL_SAFETY_PROB = 0.05       # 5% de omitir safety stop
OUTLIER_DEPTH_PROB = 0.02     # 2% de profundidades atípicas (>60m)


def simular_inmersion(inmersion_id: str):
    prof = 0.0
    t_total = 0
    aire = 300.0
    out_of_air = False

    temp = random.uniform(*RANGO_TEMPERATURA)
    nivel = random.choice(NIVELES_EXPERIENCIA)
    condiciones = random.choice(CONDICIONES_MAR)
    gas = random.choice(TIPOS_GAS)
    
    # con pequeña probabilidad, generar profundidad outlier
    if random.random() < OUTLIER_DEPTH_PROB:
        max_prof = random.uniform(61, 80)
    else:
        max_prof = random.choice(PROFUNDIDADES_MAX)

    tank_vol = random.choice(TANK_VOLUMES_L)

    # calcular bottom_time con ruido en estimación
    p = SURFACE_PRESSURE_BAR + (max_prof / DEPTH_PRESSURE_FACTOR)
    lpm_nom = (
        SURFACE_AIR_CONSUMPTION_LPM * p * WORKLOAD_FACTOR["fondo"]
        * GAS_FACTORS[gas] * EXPERIENCE_FACTORS[nivel] * MAR_CONDITION_FACTORS[condiciones]
    )
    bar_min_nom = lpm_nom / tank_vol

    ndl = ndl_limit(max_prof)
    max_by_air = int(aire / bar_min_nom)
    base_bottom = max(1, min(ndl, max_by_air))
    # aplicar variabilidad ±10%
    bottom_time = int(base_bottom * random.uniform(0.9, 1.1))
    bottom_time = max(1, min(bottom_time, base_bottom * 2))

    deco_required = bottom_time > ndl
    deco_performed = False
    safety_performed = False

    base = {
        "inmersion_id": inmersion_id,
        "temperatura_agua_celsius": round(temp, 1),
        "nivel_experiencia": nivel,
        "condiciones_mar": condiciones,
        "tipo_gas_usado": gas,
        "volumen_tanque_l": tank_vol
    }

    def consume(depth, phase):
        nonlocal aire, out_of_air
        used = gas_consumption(
            depth, phase,
            tipo_gas=gas,
            nivel_exp=nivel,
            condiciones_mar=condiciones,
            tank_volume=tank_vol
        )
        aire -= used
        # sensor noise aleatorio en lectura
        if random.random() < 0.01:  # 1% lecturas erróneas
            aire += random.uniform(-2, 2)
        if aire <= 0:
            aire = 0.0
            out_of_air = True

    # Fase Descenso
    while prof < max_prof:
        prof = min(max_prof, prof + DESCENT_RATE_M_PER_MIN)
        t_total += 1
        consume(prof, "descenso")
        yield _build_record(base, prof, t_total, aire, phase="descenso")

    # Fase Fondo
    for _ in range(bottom_time):
        t_total += 1
        consume(max_prof, "fondo")
        yield _build_record(base, max_prof, t_total, aire, phase="fondo")

    # Paradas Deco
    if deco_required and random.random() >= FAIL_DECO_PROB:
        for stop_prof, stop_time in required_deco_stops(max_prof):
            for _ in range(stop_time):
                t_total += 1
                consume(stop_prof, "deco_stop")
                deco_performed = True
                yield _build_record(base, stop_prof, t_total, aire,
                                     phase="deco_stop", parada="Sí")

    # Safety Stop
    if max_prof > SAFETY_STOP_DEPTH_THRESHOLD_M and random.random() >= FAIL_SAFETY_PROB:
        if prof > SAFETY_STOP_AT_DEPTH_M:
            prof = SAFETY_STOP_AT_DEPTH_M
        for _ in range(SAFETY_STOP_DURATION_MIN):
            t_total += 1
            consume(SAFETY_STOP_AT_DEPTH_M, "safety_stop")
            safety_performed = True
            yield _build_record(base, SAFETY_STOP_AT_DEPTH_M, t_total, aire,
                                 phase="safety_stop", parada="Sí")

    # Ascenso Final
    while prof > 0:
        prof = max(0.0, prof - ASCENT_RATE_M_PER_MIN)
        t_total += 1
        consume(prof, "ascenso")
        yield _build_record(base, prof, t_total, aire, phase="ascenso")

    # Resumen final
    reserve_ok = aire >= RESERVE_AIR_BAR
    inmersion_segura = (
        not out_of_air
        and (not deco_required or deco_performed)
        and (not (max_prof > SAFETY_STOP_DEPTH_THRESHOLD_M) or safety_performed)
        and reserve_ok
    )

    yield {
        **base,
        "profundidad_actual_m": 0.0,
        "tiempo_total_min": t_total,
        "aire_restante_bar": round(aire, 1),
        "deco_required":   "Sí" if deco_required else "No",
        "deco_performed":  "Sí" if deco_performed else "No",
        "safety_required":"Sí" if max_prof > SAFETY_STOP_DEPTH_THRESHOLD_M else "No",
        "safety_performed":"Sí" if safety_performed else "No",
        "out_of_air":      "Sí" if out_of_air else "No",
        "reserve_ok":      "Sí" if reserve_ok else "No",
        "inmersion_segura":"Sí" if inmersion_segura else "No"
    }


def _build_record(base, profundidad, tiempo, aire, phase, parada="No"):
    return {
        **base,
        "tipo": "fase",
        "fase": phase,
        "profundidad_actual_m": round(profundidad, 1),
        "tiempo_transcurrido_min": tiempo,
        "aire_restante_bar": round(aire, 1),
        "parada_de_seguridad": parada
    }

