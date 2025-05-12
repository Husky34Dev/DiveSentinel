import os
import sys
import pandas as pd
from pymongo import MongoClient

# Permitir imports desde la raíz del proyecto
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

def build_feature_table(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("inmersion_id")

    # Agregados numéricos
    summary = g.agg(
        profundidad_maxima=("profundidad_actual_m", "max"),
        profundidad_media=("profundidad_actual_m", "mean"),
        duracion_total_min=("tiempo_transcurrido_min", "max"),
        aire_minimo_bar=("aire_restante_bar", "min")
    )

    # Número de paradas
    deco = g["fase"].apply(lambda s: (s == "deco_stop").sum())
    safety = g["fase"].apply(lambda s: (s == "safety_stop").sum())

    # Etiquetas desde campos fusionados (resumen)
    out_of_air = g["out_of_air_resumen"].agg("last").map({"Sí": 1, "No": 0}).fillna(1).astype(int)
    reserve_ok = g["reserve_ok_resumen"].agg("last").map({"Sí": 1, "No": 0}).fillna(0).astype(int)
    label_seg  = g["inmersion_segura_resumen"].agg("last").map({"Sí": 1, "No": 0}).fillna(0).astype(int)

    # Variables de contexto (categorías y numéricas)
    contexto = g.agg(
        temperatura_agua_celsius=("temperatura_agua_celsius_resumen", "first"),
        nivel_experiencia=("nivel_experiencia_resumen", "first"),
        condiciones_mar=("condiciones_mar_resumen", "first"),
        tipo_gas_usado=("tipo_gas_usado_resumen", "first"),
        volumen_tanque_l=("volumen_tanque_l_resumen", "first")
    )

    # Unimos todo
    features = (
    summary
    .join(deco.rename("num_deco_stops"))
    .join(safety.rename("num_safety_stops"))
    .join(out_of_air.rename("out_of_air"))
    .join(reserve_ok.rename("reserve_ok"))
    .join(label_seg.rename("label_segura"))
    .join(contexto)
    .reset_index()
)


    return features


def main():
    client = MongoClient("mongodb://localhost:27017")
    db = client.scubaML
    collection = db.stream_inmersiones

    # Leer todos los documentos
    registros = list(collection.find({}))
    if not registros:
        print("❌ No se encontraron registros en MongoDB.")
        return

    df = pd.DataFrame(registros)

    # Separar fases y resúmenes
    df_fases = df[df["tipo"] == "fase"].copy()
    df_resumen = df[df["tipo"].isna()].copy()

    # Limpiar campos
    df_resumen = df_resumen.drop(columns=["_id"], errors="ignore")

    # Merge fases + resumen
    df_merged = df_fases.merge(
        df_resumen,
        on="inmersion_id",
        suffixes=("", "_resumen"),
        how="left"
    )

    # Guardar raw
    os.makedirs("data", exist_ok=True)
    raw_csv = os.path.join("data", "raw_data.csv")
    df_merged.to_csv(raw_csv, index=False)
    print(f"📄 Raw data guardado en {raw_csv}")

    # Generar features
    df_feats = build_feature_table(df_merged)

    # Guardar features
    feats_csv = os.path.join("data", "features_dataset.csv")
    df_feats.to_csv(feats_csv, index=False)
    print(f"✅ Dataset de features guardado en {feats_csv}")


if __name__ == "__main__":
    main()
