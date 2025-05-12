# scripts/generar_datos_stream.py

import os
import sys
import time
import logging
import requests

# 1) Hacer que Python encuentre el paquete src/
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from src.simulator.simulator import simular_inmersion
from src.config import API_URL

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO
)

def main():
    inmersiones = [f"SIM_{i:03d}" for i in range(202, 1001)]
    for inm_id in inmersiones:
        logging.info(f"[{inm_id}] arrancando simulación")
        for registro in simular_inmersion(inm_id):
            try:
                url = f"{API_URL}/stream"
                resp = requests.post(url, json=registro, timeout=5)
                resp.raise_for_status()
                logging.debug(f"  ✔ enviado: prof={registro['profundidad_actual_m']}m")
            except Exception as e:
                logging.error(f"  ✖ fallo al enviar registro: {e}")

    logging.info(">> FIN de todas las simulaciones <<")

if __name__ == "__main__":
    main()
