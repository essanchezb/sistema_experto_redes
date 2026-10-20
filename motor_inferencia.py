
"""
Motor de inferencia del sistema experto de redes.
Evalua hechos, selecciona reglas y genera conclusiones.
"""

import random


def motor_inferencia(hechos_iniciales, reglas):
    # NUEVO: guardar los hechos conocidos sin duplicados.
    hechos = set(hechos_iniciales)

    # NUEVO: distinguir hechos iniciales de hechos deducidos.
    hechos_iniciales_set = set(hechos_iniciales)
    hechos_deducidos = set()

    # NUEVO: impedir que una misma regla se ejecute varias veces.
    reglas_ejecutadas = set()

    # NUEVO: registrar cada paso para mostrar el razonamiento.
    historial = []

    while True:
        # Buscar las reglas que pueden aplicarse.
        conjunto_conflicto = [
            regla for regla in reglas
            if regla["id"] not in reglas_ejecutadas
            and set(regla["antecedentes"]).issubset(hechos)
        ]

        # Si no hay reglas aplicables, termina la inferencia.
        if not conjunto_conflicto:
            break

        # Estrategia 1: elegir la prioridad más alta.
        prioridad_maxima = max(
            regla.get("prioridad", 0)
            for regla in conjunto_conflicto
        )

        candidatas = [
            regla for regla in conjunto_conflicto
            if regla.get("prioridad", 0) == prioridad_maxima
        ]

        # Estrategia 2: preferir la regla más específica,
        # es decir, la que tiene más antecedentes.
        max_antecedentes = max(
            len(regla["antecedentes"])
            for regla in candidatas
        )

        candidatas = [
            regla for regla in candidatas
            if len(regla["antecedentes"]) == max_antecedentes
        ]

        # Estrategia 3: preferir reglas que usen hechos
        # deducidos durante la inferencia.
        max_recientes = max(
            len(set(regla["antecedentes"]) & hechos_deducidos)
            for regla in candidatas
        )

        candidatas = [
            regla for regla in candidatas
            if len(set(regla["antecedentes"]) & hechos_deducidos)
            == max_recientes
        ]

        # Estrategia 4: desempate aleatorio entre las candidatas.
        regla = random.choice(candidatas)

        # Registrar la regla como ejecutada.
        reglas_ejecutadas.add(regla["id"])

        # Obtener los hechos que esta regla permite deducir.
        nuevos_hechos = (
            set(regla["consecuentes"]) - hechos
        )

        # Registrar el paso, incluso si no produce hechos nuevos.
        historial.append({
            "regla": regla["id"],
            "nombre": regla["nombre"],
            "antecedentes": regla["antecedentes"],
            "consecuentes": regla["consecuentes"],
            "nuevos_hechos": sorted(nuevos_hechos),
            "prioridad": regla.get("prioridad", 0)
        })

        # Incorporar los nuevos hechos a la memoria de trabajo.
        hechos.update(nuevos_hechos)
        hechos_deducidos.update(nuevos_hechos)

    return {
        "hechos_iniciales": sorted(hechos_iniciales_set),
        "hechos_deducidos": sorted(hechos_deducidos),
        "hechos_finales": sorted(hechos),
        "historial": historial
    }
