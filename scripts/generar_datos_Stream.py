import requests
import time
import random

API_URL = "http://localhost:5001/stream"

def simular_inmersion(inmersion_id):
    """Simula una inmersión con un descenso controlado, tiempo en fondo y ascenso seguro."""

    # 🔵 **Parámetros de la inmersión**
    profundidad_actual = 0
    tiempo_total = 0
    aire_restante = 200  # Bar inicial
    ritmo_cardiaco = 80  # BPM inicial
    temperatura_agua = random.uniform(15, 25)
    nivel_experiencia = random.choice(["Principiante", "Intermedio", "Avanzado"])
    condiciones_mar = random.choice(["Calmado", "Moderado", "Agitado"])
    tipo_gas = random.choice(["Aire", "Nitrox", "Trimix"])
    max_profundidad = random.choice([10, 20, 30, 40])

    print(f"🚀 Iniciando inmersión ID: {inmersion_id}, Profundidad objetivo: {max_profundidad}m")

    # 🔽 **FASE 1: DESCENSO**
    while profundidad_actual < max_profundidad:
        print(f"⬇️ Descendiendo... Profundidad actual: {profundidad_actual}m")
        incremento = random.uniform(5, 10)  # Desciende de 5 a 10 m/min
        profundidad_actual = min(profundidad_actual + incremento, max_profundidad)
        tiempo_total += 1
        aire_restante -= random.uniform(2, 5)
        ritmo_cardiaco += random.uniform(2, 5)

        enviar_dato(inmersion_id, profundidad_actual, tiempo_total, temperatura_agua,
                    aire_restante, ritmo_cardiaco, nivel_experiencia, condiciones_mar, tipo_gas, "No", "Sí")

        time.sleep(0.5)

    print(f"🔵 Estabilización en fondo por {random.randint(5, 20)} minutos")

    # 🏊‍♂️ **FASE 2: PERMANENCIA EN EL FONDO**
    fondo_duracion = random.randint(5, 20)
    for _ in range(fondo_duracion):
        print(f"⏳ En el fondo... Tiempo transcurrido: {tiempo_total} min")
        tiempo_total += 1
        aire_restante -= random.uniform(2, 6)

        enviar_dato(inmersion_id, max_profundidad, tiempo_total, temperatura_agua,
                    aire_restante, ritmo_cardiaco, nivel_experiencia, condiciones_mar, tipo_gas, "No", "Sí")

        time.sleep(0.5)

    # 🆙 **FASE 3: ASCENSO CON PARADAS**
    while profundidad_actual > 0:
        print(f"⬆️ Ascendiendo... Profundidad actual: {profundidad_actual}m")
        if profundidad_actual > 10 and profundidad_actual % 10 == 0:
            paradas_seguridad = "Sí"
            pausa = random.randint(2, 5)
        else:
            paradas_seguridad = "No"
            pausa = 1

        profundidad_actual -= 5
        tiempo_total += pausa
        aire_restante -= random.uniform(1, 3)
        ritmo_cardiaco -= random.uniform(1, 4)

        if profundidad_actual < 0:
            profundidad_actual = 0  # Asegurar que termina en la superficie

        enviar_dato(inmersion_id, profundidad_actual, tiempo_total, temperatura_agua,
                    aire_restante, ritmo_cardiaco, nivel_experiencia, condiciones_mar, tipo_gas, paradas_seguridad, "Sí")

        time.sleep(0.5)

    print(f"✅ Inmersión {inmersion_id} completada y enviada a MongoDB.")


def enviar_dato(inmersion_id, profundidad, tiempo, temp, aire, ritmo, exp, mar, gas, paradas, ascenso):
    """Envía un dato de inmersión a la API Flask."""
    dato = {
        "inmersion_id": inmersion_id,
        "Profundidad_maxima_m": round(profundidad, 1),
        "Tiempo_fondo_min": tiempo,
        "Temperatura_agua_C": round(temp, 1),
        "Consumo_aire_bar": round(aire, 1),
        "Ritmo_cardiaco_bpm": round(ritmo, 1),
        "Nivel_experiencia": exp,
        "Condiciones_mar": mar,
        "Tipo_gas": gas,
        "Paradas_seguridad": paradas,
        "Ascenso_controlado": ascenso
    }

    try:
        response = requests.post(API_URL, json=dato)
        print(f"📤 Enviando dato: {dato} | Respuesta: {response.status_code}")
        if response.status_code != 201:
            print(f"⚠️ Error en la API: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

# Ejecutar simulación
if __name__ == "__main__":
    simular_inmersion("TEST456")
