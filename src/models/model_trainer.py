import os
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score
import joblib

# 1) Carga de datos
data_path = 'data/features_dataset.csv'
df = pd.read_csv(data_path)

# 2) Variables
numerical_feats = ['temperatura_agua_celsius', 'volumen_tanque_l', 'profundidad_maxima']
categorical_feats = ['nivel_experiencia', 'condiciones_mar', 'tipo_gas_usado']

X = df[numerical_feats + categorical_feats]
y = df['label_segura']

# 3) División estratificada
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4) Preprocesado
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numerical_feats),
    ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_feats)
], remainder='drop')

# 5) Pipeline de entrenamiento
model = HistGradientBoostingClassifier(random_state=42)
pipeline = Pipeline([
    ('prep', preprocessor),
    ('clf', model)
])

# 6) Búsqueda de hiperparámetros
param_dist = {
    'clf__learning_rate': [0.01, 0.05, 0.1],
    'clf__max_iter': [100, 200],
    'clf__max_depth': [None, 5, 10],
    'clf__min_samples_leaf': [20, 50],
    'clf__l2_regularization': [0.0, 0.1]
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
search = RandomizedSearchCV(
    pipeline, param_dist, n_iter=10, cv=cv,
    scoring='roc_auc', n_jobs=-1, random_state=42, verbose=1
)

# 7) Entrenamiento
search.fit(X_train, y_train)
print("✔️ Mejores parámetros:", search.best_params_)

# 8) Evaluación
best = search.best_estimator_
y_pred = best.predict(X_test)
y_proba = best.predict_proba(X_test)[:, 1]

print(f"📊 Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(f"📈 ROC AUC: {roc_auc_score(y_test, y_proba):.3f}")
print(classification_report(y_test, y_pred))

# 9) Guardado
os.makedirs('src/models', exist_ok=True)
model_path = os.getenv('MODEL_PATH', 'src/models/pipeline_gbc.joblib')
joblib.dump(best, model_path)
print(f"💾 Modelo guardado en {model_path}")
