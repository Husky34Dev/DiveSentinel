# src/routes/routes.py

from flask import request, jsonify
from src.services.db_service import insertar_inmersion, obtener_historial

def initialize_routes(app):
    @app.route("/ping", methods=["GET"])
    def ping():
        return jsonify({"message": "API funcionando"}), 200

   
    @app.route("/historial", methods=["GET"])
    def historial():
        datos = obtener_historial()
        return jsonify(datos), 200

   