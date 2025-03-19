# ScubaML - Análisis de Seguridad en Inmersiones de Buceo con Machine Learning

## 📌 Descripción del Proyecto
ScubaML es una aplicación basada en Machine Learning y procesamiento de datos en tiempo real para evaluar la seguridad de inmersiones de buceo. Utiliza un flujo de datos en vivo que registra métricas críticas durante la inmersión y posteriormente genera un análisis automatizado sobre la seguridad de la inmersión.

## 🏗️ Arquitectura del Proyecto
El sistema está compuesto por:
- **Flask API**: Para recibir y procesar datos en tiempo real.
- **MongoDB**: Para almacenar las inmersiones y sus eventos.
- **Machine Learning**: Un modelo de clasificación entrenado con Random Forest para evaluar la seguridad de la inmersión.
- **Streaming de Datos**: Un sistema que simula y envía datos de una inmersión realista en tiempo real.

## 📂 Estructura del Proyecto
```
scubaML/
│── src/
│   ├── app.py  # Archivo principal para ejecutar la API Flask
│   ├── routes/
│   │   ├── routes.py  # Endpoints principales
│   │   ├── stream_routes.py  # Manejo de datos en tiempo real
│   ├── services/
│   │   ├── db_service.py  # Conexión con MongoDB
│   │   ├── evaluation_service.py  # Reglas de evaluación de seguridad
│   │   ├── inmersion_analysis.py  # Análisis de los datos de la inmersión
│   ├── models/
│   │   ├── model_trainer.py  # Entrenamiento del modelo ML
│   │   ├── predict.py  # Predicción con el modelo entrenado
│── scripts/
│   ├── generar_inmersion_realista.py  # Script para simular inmersiones en tiempo real
│── data/
│   ├── dataset_inmersiones.csv  # Dataset de entrenamiento
│── README.md  # Documentación del proyecto
│── requirements.txt  # Dependencias del proyecto
```

## 🚀 Instalación y Configuración
### **1️⃣ Clonar el repositorio**
```bash
git clone https://github.com/tu_usuario/scubaML.git
cd scubaML
```
### **2️⃣ Crear un entorno virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate  # Windows
```
### **3️⃣ Instalar dependencias**
```bash
pip install -r requirements.txt
```
### **4️⃣ Configurar MongoDB**
Asegúrate de que MongoDB está corriendo:
```bash
mongod --dbpath "C:\data\db"  # Windows
sudo systemctl start mongod  # Linux
```
Crear la base de datos y las colecciones necesarias:
```bash
mongosh
use scubaML
db.createCollection("stream_inmersiones")
db.createCollection("historial_inmersiones")
```

## 🌊 Flujo de Trabajo
1️⃣ **Se inicia la API Flask**
```bash
python src/app.py
```
2️⃣ **Se simula una inmersión con datos en tiempo real**
```bash
python scripts/generar_inmersion_realista.py
```
3️⃣ **Se consulta el historial de inmersiones**
```bash
curl -X GET http://localhost:5000/historial
```
4️⃣ **Se evalúa la seguridad de una inmersión**
```bash
curl -X GET http://localhost:5000/finalizar_inmersion/TEST123
```

## 📊 Datos Recopilados
Cada inmersión genera datos en tiempo real con los siguientes parámetros:
- **Profundidad máxima (m)**
- **Tiempo transcurrido (min)**
- **Temperatura del agua (°C)**
- **Consumo de aire (bar)**
- **Ritmo cardíaco (bpm)**
- **Nivel de experiencia del buceador**
- **Condiciones del mar**
- **Tipo de gas respirado (Aire, Nitrox, Trimix)**
- **Paradas de seguridad realizadas**
- **Ascenso controlado o no**

## 🧠 Machine Learning
- Se utiliza **Random Forest** para clasificar una inmersión como **Segura o No Segura**.
- Se entrenó con un dataset generado sintéticamente basado en reglas de buceo.
- Se optimizó con **RandomizedSearchCV** para ajustar hiperparámetros.

## 📌 Próximos Pasos
✅ Mejorar el modelo ML con más datos reales.
✅ Agregar una interfaz gráfica para visualizar las inmersiones.
✅ Implementar alertas en tiempo real para prevenir inmersiones peligrosas.

---

👨‍💻 **Desarrollado por:** Bernardo Martínez Romero  
🌐 **Repositorio en GitHub:** [[Enlace a tu repo](https://github.com/Husky34Dev/SCUBAML)]