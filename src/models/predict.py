# src/models/predict_from_mongo.py

import pandas as pd
import joblib
from pymongo import MongoClient

MODEL_PATH = "src/models/pipeline_gbc.joblib"
pipeline = joblib.load(MODEL_PATH)

def predecir_seguridad_desde_mongo(inmersion_id: str) -> str:
    client = MongoClient("mongodb://localhost:27017")
    db = client.scubaML
    col = db.stream_inmersiones

    # Fases
    fases_df = pd.DataFrame(col.find({"inmersion_id": inmersion_id, "tipo": "fase"}))
    if fases_df.empty:
        return f"❌ No se encontraron fases para {inmersion_id}"

    # Resumen final (donde está out_of_air, reserve_ok...)
    resumen = col.find_one({"inmersion_id": inmersion_id, "tipo": {"$exists": False}})
    if not resumen:
        return f"⚠️ No se encontró resumen para {inmersion_id}"

    # Extraer features
    features = {
        "profundidad_maxima": fases_df["profundidad_actual_m"].max(),
        "profundidad_media": fases_df["profundidad_actual_m"].mean(),
        "duracion_total_min": fases_df["tiempo_transcurrido_min"].max(),
        "aire_minimo_bar": fases_df["aire_restante_bar"].min(),
        "num_deco_stops": (fases_df["fase"] == "deco_stop").sum(),
        "num_safety_stops": (fases_df["fase"] == "safety_stop").sum(),
        "out_of_air": 1 if resumen["out_of_air"] == "Sí" else 0,
        "reserve_ok": 1 if resumen["reserve_ok"] == "Sí" else 0,
        "temperatura_agua_celsius": resumen["temperatura_agua_celsius"],
        "nivel_experiencia": resumen["nivel_experiencia"],
        "condiciones_mar": resumen["condiciones_mar"],
        "tipo_gas_usado": resumen["tipo_gas_usado"],
        "volumen_tanque_l": resumen["volumen_tanque_l"]
    }

    input_df = pd.DataFrame([features])
    pred = pipeline.predict(input_df)[0]
    return f"✅ La inmersión {inmersion_id} {'fue' if pred else 'NO fue'} segura."

# Ejemplo de uso
if __name__ == "__main__":
    print(predecir_seguridad_desde_mongo("SIM_403")) 

