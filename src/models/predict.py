# src/models/predict.py

import joblib
import numpy as np
import pandas as pd

# Cargar el modelo entrenado
MODEL_PATH = "src/models/model_rf.pkl"
clf = joblib.load(MODEL_PATH)

# Mapeo para transformar valores categóricos
def preprocess_input(data):
    """Convierte datos de una nueva inmersión en el formato adecuado para el modelo."""
    mapping_experiencia = {"Principiante": 0, "Intermedio": 1, "Avanzado": 2}
    mapping_gas = {"Aire": 0, "Nitrox": 1, "Trimix": 2}
    mapping_si_no = {"Sí": 1, "No": 0}
    mapping_mar = {"Calmado": 0, "Moderado": 1, "Agitado": 2}

    processed_data = {
        "Profundidad_maxima_m": data.get("Profundidad_maxima_m", 0),
        "Tiempo_fondo_min": data.get("Tiempo_fondo_min", 0),
        "Temperatura_agua_C": data.get("Temperatura_agua_C", 0),
        "Consumo_aire_bar": data.get("Consumo_aire_bar", 0),
        "Ritmo_cardiaco_bpm": data.get("Ritmo_cardiaco_bpm", 70),
        "Nivel_experiencia": mapping_experiencia.get(data.get("Nivel_experiencia", "Principiante"), 0),
        "Condiciones_mar": mapping_mar.get(data.get("Condiciones_mar", "Calmado"), 0),
        "Tipo_gas": mapping_gas.get(data.get("Tipo_gas", "Aire"), 0),
        "Paradas_seguridad": mapping_si_no.get(data.get("Paradas_seguridad", "Sí"), 1),
        "Ascenso_controlado": mapping_si_no.get(data.get("Ascenso_controlado", "Sí"), 1)
    }
    
    processed_data["Nivel_experiencia_peso"] = processed_data["Nivel_experiencia"] * 2

    return pd.DataFrame([processed_data])

# Función de predicción
def predecir_seguridad(data):
    """Hace una predicción sobre la seguridad de la inmersión."""
    input_data = preprocess_input(data)
    prediction = clf.predict(input_data)[0]
    return "Sí" if prediction == 1 else "No"
