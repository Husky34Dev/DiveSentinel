# src/services/evaluation_service.py

def evaluar_inmersion(datos):
    """
    Evalúa si una inmersión es segura o peligrosa según las reglas establecidas.

    Parámetro:
        datos (dict): Información de la inmersión.

    Retorna:
        dict: Resultado con 'segura' (Sí/No) y detalles.
    """
    profundidad = datos.get("Profundidad_maxima_m", 0)
    ascenso_controlado = datos.get("Ascenso_controlado", "Sí")
    paradas_seguridad = datos.get("Paradas_seguridad", "Sí")
    tipo_gas = datos.get("Tipo_gas", "Aire")
    ritmo_cardiaco = datos.get("Ritmo_cardiaco_bpm", 70)
    consumo_aire = datos.get("Consumo_aire_bar", 100)
    condiciones_mar = datos.get("Condiciones_mar", "Calmado")
    nivel_experiencia = datos.get("Nivel_experiencia", "Principiante")

    # Lista de razones si la inmersión es peligrosa
    razones_peligro = []

    # 🚨 1️⃣ Validación de profundidad extrema
    if profundidad > 100:
        razones_peligro.append("Profundidad extrema detectada (>100m), inmersión inviable con equipo convencional.")

    # 🚨 2️⃣ Validación del tipo de gas y la profundidad
    if tipo_gas == "Aire" and profundidad > 30:
        razones_peligro.append("Uso de Aire por encima de 30m, posible narcosis nitrogenosa y riesgo de toxicidad de oxígeno.")
    if tipo_gas == "Nitrox" and profundidad > 40:
        razones_peligro.append("Uso de Nitrox por encima de 40m, posible toxicidad del oxígeno.")
    if tipo_gas == "Trimix" and profundidad > 100:
        razones_peligro.append("Incluso con Trimix, esta profundidad es extrema y peligrosa.")

    # 🚨 3️⃣ Riesgo por ascenso incontrolado
    if ascenso_controlado == "No":
        razones_peligro.append("Ascenso incontrolado detectado (riesgo de embolia).")

    # 🚨 4️⃣ Falta de paradas de seguridad en inmersiones profundas
    if profundidad > 30 and paradas_seguridad == "No":
        razones_peligro.append("No se realizaron paradas de seguridad en inmersión profunda.")

    # 🚨 5️⃣ Ritmo cardíaco elevado
    if ritmo_cardiaco > 160:
        razones_peligro.append("Ritmo cardíaco elevado (>160 bpm), posible estrés o pánico.")

    # 🚨 6️⃣ Consumo de aire excesivo
    if consumo_aire > 150:
        razones_peligro.append("Consumo de aire excesivo (>150 bar), reserva de seguridad comprometida.")
    
    # 🚨 8️⃣ Restricción por nivel de experiencia y tipo de gas
    if nivel_experiencia == "Principiante" and tipo_gas in ["Nitrox", "Trimix"]:
        razones_peligro.append("Un principiante no debe usar Nitrox o Trimix sin experiencia adecuada.")
    if nivel_experiencia == "Intermedio" and tipo_gas == "Trimix":
        razones_peligro.append("Un buceador intermedio no debería usar Trimix sin entrenamiento técnico.")

    # 🚨 9️⃣ Evaluación de condiciones del mar en combinación con experiencia y profundidad
    if condiciones_mar == "Agitado":
        if profundidad > 25:
            razones_peligro.append("Mar agitado y profundidad superior a 25m, posible dificultad para ascender.")
        elif nivel_experiencia == "Principiante" and profundidad > 10:
            razones_peligro.append("Principiante en mar agitado con profundidad mayor a 10m, riesgo elevado.")
        elif nivel_experiencia == "Intermedio" and profundidad > 20:
            razones_peligro.append("Buceador intermedio en mar agitado con profundidad mayor a 20m, riesgo moderado.")
    
    # Determinar resultado final
    segura = "No" if razones_peligro else "Sí"

    return {
        "segura": segura,
        "razones": razones_peligro
    }