import pandas as pd

def analizar_inmersion(datos):
    """Toma los datos crudos de la inmersión y genera un resumen para la predicción."""
    
    df = pd.DataFrame(datos)

    # Calcular velocidad de descenso/ascenso
    df["Diferencia_profundidad"] = df["Profundidad_maxima_m"].diff()
    df["Velocidad_ascenso"] = df["Diferencia_profundidad"] / df["Tiempo_fondo_min"].diff()
    df["Velocidad_descenso"] = df["Diferencia_profundidad"].apply(lambda x: x if x > 0 else 0)

    # Verificar si se hicieron paradas de seguridad
    df["Parada_seguridad"] = (df["Profundidad_maxima_m"] < 5).astype(int)
    hizo_paradas = df["Parada_seguridad"].sum() > 0

    # Evaluar cambios en el ritmo cardíaco
    variabilidad_ritmo = df["Ritmo_cardiaco_bpm"].std()

    # Evaluar consumo de aire total
    consumo_total = df["Consumo_aire_bar"].sum()

    # Generar resumen
    resumen = {
        "Profundidad_maxima_m": df["Profundidad_maxima_m"].max(),
        "Tiempo_fondo_min": df["Tiempo_fondo_min"].max(),
        "Temperatura_agua_C": df["Temperatura_agua_C"].mean(),
        "Consumo_aire_bar": consumo_total,
        "Ritmo_cardiaco_bpm": df["Ritmo_cardiaco_bpm"].mean(),
        "Nivel_experiencia": df["Nivel_experiencia"].iloc[0],
        "Condiciones_mar": df["Condiciones_mar"].iloc[0],
        "Tipo_gas": df["Tipo_gas"].iloc[0],
        "Paradas_seguridad": "Sí" if hizo_paradas else "No",
        "Ascenso_controlado": "No" if df["Velocidad_ascenso"].max() > 10 else "Sí",
    }

    return resumen
