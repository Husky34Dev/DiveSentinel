import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Cargar dataset
DATASET_PATH = "data/dataset_inmersiones.csv"
df = pd.read_csv(DATASET_PATH)

# 🚨 Agregar datos sintéticos de inmersiones extremas para que el modelo aprenda
extra_data = pd.DataFrame([
    {"Profundidad_maxima_m": 120, "Tiempo_fondo_min": 80, "Temperatura_agua_C": 5, "Consumo_aire_bar": 180,
     "Ritmo_cardiaco_bpm": 150, "Nivel_experiencia": "Avanzado", "Condiciones_mar": "Moderado", "Tipo_gas": "Trimix",
     "Paradas_seguridad": "No", "Ascenso_controlado": "No", "Inmersion_segura": "No"},
    {"Profundidad_maxima_m": 200, "Tiempo_fondo_min": 90, "Temperatura_agua_C": 2, "Consumo_aire_bar": 200,
     "Ritmo_cardiaco_bpm": 160, "Nivel_experiencia": "Avanzado", "Condiciones_mar": "Agitado", "Tipo_gas": "Trimix",
     "Paradas_seguridad": "No", "Ascenso_controlado": "No", "Inmersion_segura": "No"},
])
df = pd.concat([df, extra_data], ignore_index=True)

# Mapeo de valores categóricos
def preprocess_data(df):
    """ Preprocesa el dataset convirtiendo variables categóricas en numéricas. """
    mapping_experiencia = {"Principiante": 0, "Intermedio": 1, "Avanzado": 2}
    mapping_gas = {"Aire": 0, "Nitrox": 1, "Trimix": 2}
    mapping_si_no = {"Sí": 1, "No": 0}
    mapping_mar = {"Calmado": 0, "Moderado": 1, "Agitado": 2}

    df["Nivel_experiencia"] = df["Nivel_experiencia"].map(mapping_experiencia)
    df["Tipo_gas"] = df["Tipo_gas"].map(mapping_gas)
    df["Paradas_seguridad"] = df["Paradas_seguridad"].map(mapping_si_no)
    df["Ascenso_controlado"] = df["Ascenso_controlado"].map(mapping_si_no)
    df["Inmersion_segura"] = df["Inmersion_segura"].map(mapping_si_no)
    df["Condiciones_mar"] = df["Condiciones_mar"].map(mapping_mar)

    return df

# Preprocesar datos
df = preprocess_data(df)

# Separar características (X) y etiqueta de clasificación (y)
X = df.drop(columns=["Inmersion_segura", "ID_inmersion"], errors="ignore")

# Aumentar peso de la experiencia en el modelo
X["Nivel_experiencia_peso"] = X["Nivel_experiencia"] * 2  

# Penalización de seguridad para principiantes en inmersiones peligrosas
df["Penalizacion_seguridad"] = df.apply(
    lambda row: 3 if row["Nivel_experiencia"] == 0 and row["Inmersion_segura"] == 0 else 1, axis=1
)

# Aplicar la penalización en la clasificación
y = df["Inmersion_segura"] * df["Penalizacion_seguridad"]

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🚀 Optimización de hiperparámetros con RandomizedSearchCV
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

rf = RandomForestClassifier(random_state=42)
grid_search = RandomizedSearchCV(estimator=rf, param_distributions=param_grid, 
                                 n_iter=10, cv=5, verbose=2, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Mejor modelo optimizado
best_rf = grid_search.best_estimator_

# Evaluar modelo
y_pred = best_rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo después de optimización: {accuracy:.2f}")
print(classification_report(y_test, y_pred))

# Guardar el modelo optimizado
MODEL_PATH = "src/models/model_rf.pkl"
joblib.dump(best_rf, MODEL_PATH)
print(f"Modelo optimizado guardado en {MODEL_PATH}")
