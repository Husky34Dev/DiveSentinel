# DiveSentinel - Seguridad Inteligente para Inmersiones de Buceo

## 📌 Descripción del Proyecto  
DiveSentinel es un sistema de análisis inteligente que utiliza Machine Learning para evaluar si una inmersión de buceo ha sido segura o no. Ante la falta de datasets reales, se desarrolló un simulador completo que genera inmersiones sintéticas basadas en modelos reales de buceo técnico como el algoritmo de Bühlmann, consumo de gases, paradas de descompresión y más.

## 🏗️ Arquitectura del Proyecto  
El sistema está compuesto por:
- **Flask API**: Recibe solicitudes y ofrece predicciones sobre la seguridad de una inmersión.
- **MongoDB**: Almacena los datos crudos minuto a minuto de cada inmersión.
- **Machine Learning (HistGradientBoostingClassifier)**: Modelo entrenado con inmersiones simuladas.
- **Scripts de simulación y extracción**: Generan los datos y preparan el dataset para el entrenamiento.

## 📂 Estructura del Proyecto

```
DiveSentinel/
├── data/
│   ├── features_dataset.csv
│   └── raw_data.csv
│
├── scripts/
│   ├── generar_dataset.py
│   └── generar_datos_stream.py
│
├── src/
│   ├── controllers/
│   ├── models/
│   │   ├── model_rf.pkl
│   │   ├── model_trainer.py
│   │   ├── pipeline_gbc.joblib
│   │   └── predict.py
│   ├── routes/
│   │   ├── init.py
│   │   ├── routes.py
│   │   └── stream_routes.py
│   ├── services/
│   │   ├── init.py
│   │   ├── api_client.py
│   │   └── db_service.py
│   ├── simulator/
│   │   ├── init.py
│   │   └── simulator.py
│   ├── utils/
│   │   ├── init.py
│   │   └── simulation_utils.py
│   ├── app.py
│   └── config.py
│
├── requirements.txt
├── setup.py
├── README.md
└── tests/
```

## 🚀 Instalación y Configuración

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/Husky34Dev/DiveSentinel.git
cd DiveSentinel
```

### 2️⃣ Crear entorno virtual e instalar dependencias
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

### 3️⃣ Configurar MongoDB
Asegúrate de tener MongoDB ejecutándose localmente. Por defecto, DiveSentinel usa la URI `mongodb://localhost:27017` y accede a la base de datos `scubaML`.

Puedes crear la colección manualmente desde la shell de Mongo:

```bash
mongosh
use scubaML
db.createCollection("stream_inmersiones")
```

---

## 🌊 Flujo de Trabajo

1. **Iniciar la API Flask**  
   ```bash
   python src/app.py
   ```

2. **Simular una inmersión**  
   ```bash
   python scripts/generar_datos_stream.py
   ```

3. **Extraer y procesar datos desde MongoDB**  
   ```bash
   python scripts/generar_dataset.py
   ```

4. **Entrenar el modelo**  
   ```bash
   python src/models/model_trainer.py
   ```

5. **Predecir la seguridad de una inmersión existente**  
   ```bash
   curl -X GET http://localhost:5000/predict/inmersion_SIM_001
   ```

---

## 📊 Variables Recolectadas

Durante cada inmersión se registran:
- Profundidad máxima y media
- Tiempo total
- Consumo mínimo de aire
- Número de paradas de seguridad y descompresión
- Condiciones del mar
- Tipo de gas utilizado
- Temperatura del agua
- Nivel de experiencia del buceador
- Resultado final: **Segura (1) / No segura (0)**

---

## 🧠 Machine Learning

- **Modelo**: HistGradientBoostingClassifier (scikit-learn)  
- **Entrenado con**: `features_dataset.csv` generado desde datos simulados  
- **Optimización automática**: RandomizedSearchCV  
- **Output**: Binario (Segura / No segura)

---

## 🧩 Próximos Pasos

- Incluir datos reales en el entrenamiento  
- Desplegar el sistema como plataforma web (SaaS)  
- Crear interfaz visual para instructores y centros de buceo  
- Añadir notificaciones y alertas automáticas

---

👨‍💻 **Desarrollado por**: Bernardo Martínez Romero  
🔗 **Repositorio GitHub**: https://github.com/Husky34Dev/DiveSentinel
