# src/routes/routes.py

from flask import request, jsonify
from services.db_service import insertar_inmersion, obtener_historial
from services.evaluation_service import evaluar_inmersion
from models.predict import predecir_seguridad

def initialize_routes(app):
    """Define las rutas de la API."""

    @app.route("/ping", methods=["GET"])
    def ping():
        return jsonify({"message": "API funcionando"}), 200

    @app.route("/inmersion", methods=["POST"])
    def nueva_inmersion():
        """
        Recibe los datos de una inmersión, evalúa su seguridad y la guarda en MongoDB.
        """
        datos = request.json
        evaluacion = evaluar_inmersion(datos)
        prediccion_ml = predecir_seguridad(datos)

        datos["Inmersion_segura_reglas"] = evaluacion["segura"]
        datos["Razones_peligro"] = evaluacion["razones"]
        datos["Inmersion_segura_ml"] = prediccion_ml  # Predicción del modelo

        inmersion_id = insertar_inmersion(datos)

        return jsonify({
            "message": "Inmersión guardada",
            "id": str(inmersion_id),
            "segura_reglas": evaluacion["segura"],
            "razones": evaluacion["razones"],
            "segura_ml": prediccion_ml
        }), 201

    @app.route("/historial", methods=["GET"])
    def historial():
        """Devuelve todas las inmersiones almacenadas."""
        datos = obtener_historial()
        return jsonify(datos), 200

    @app.route("/predict", methods=["POST"])
    def predict():
        """
        Recibe datos de una inmersión y devuelve la predicción del modelo de IA.
        """
        datos = request.json
        prediccion = predecir_seguridad(datos)

        return jsonify({
            "message": "Predicción realizada",
            "segura_ml": prediccion
        }), 200