from pymongo import MongoClient

# 🚀 Conectar a MongoDB
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)

# Seleccionar la base de datos
db = client["scubaML"]

# Definir colecciones
collection_stream = db["stream_inmersiones"]
collection_historial = db["historial_inmersiones"]

def insertar_dato_inmersion(datos):
    """Guarda un dato en la colección de streaming."""
    collection_stream.insert_one(datos)

def obtener_inmersion_completa(inmersion_id):
    """Obtiene todos los datos registrados para una inmersión específica."""
    return list(collection_stream.find({"inmersion_id": inmersion_id}, {"_id": 0}))

def insertar_inmersion(datos):
    """Guarda un resumen final de la inmersión en el historial."""
    return collection_historial.insert_one(datos).inserted_id

def obtener_historial():
    """Devuelve todas las inmersiones almacenadas en la base de datos."""
    return list(collection_historial.find({}, {"_id": 0}))
