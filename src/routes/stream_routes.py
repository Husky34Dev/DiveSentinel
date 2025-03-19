from flask import request, jsonify
from services.db_service import insertar_dato_inmersion, obtener_inmersion_completa
import datetime

def initialize_stream_routes(app):
    """Define las rutas para manejar el stream de datos de la inmersión."""

    def registrar_dato():
        """
        Recibe datos en tiempo real durante la inmersión y los almacena en MongoDB.
        """
        datos = request.json
        datos["timestamp"] = datetime.datetime.utcnow()  # Añadir marca de tiempo

        insertar_dato_inmersion(datos)

        return jsonify({"message": "Dato registrado correctamente"}), 201

    def obtener_inmersion(inmersion_id):
        """
        Obtiene todos los datos registrados para una inmersión específica.
        """
        datos = obtener_inmersion_completa(inmersion_id)

        return jsonify(datos), 200

    app.add_url_rule('/stream', 'registrar_dato', registrar_dato, methods=['POST'])
    app.add_url_rule('/inmersion/<inmersion_id>', 'obtener_inmersion', obtener_inmersion, methods=['GET'])