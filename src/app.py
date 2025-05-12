import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask
from flask_cors import CORS

from src.routes.routes import initialize_routes
from src.routes.stream_routes import initialize_stream_routes

app = Flask(__name__)
CORS(app)

# 3) Registramos las rutas
initialize_routes(app)
initialize_stream_routes(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
