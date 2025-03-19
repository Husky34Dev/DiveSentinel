from flask import Flask
from flask_cors import CORS
from routes.routes import initialize_routes
from routes.stream_routes import initialize_stream_routes

app = Flask(__name__)
CORS(app)  # Permitir CORS para comunicación con frontend

# Inicializamos las rutas
initialize_routes(app)
initialize_stream_routes(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
