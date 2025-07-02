import math
import random
from copy import deepcopy
from models.solution import TransportSolution
from utils.repair import reparar_asignacion

def simulated_annealing(initial_solution: TransportSolution, T_inicial=1000, T_final=1, alpha=0.95, iteraciones=100):
    actual = initial_solution.clone()
    costo_actual = actual.costo_total()

    mejor = actual.clone()
    mejor_costo = costo_actual

    T = T_inicial
    historico = []

    while T > T_final:
        for _ in range(iteraciones):
            vecino = generar_vecino(actual)

            # Reparar para garantizar que cumpla restricciones
            vecino = reparar_asignacion(vecino)

            if not vecino.is_valid():
                continue  # si sigue inválido, saltar

            costo_vecino = vecino.costo_total()
            delta = costo_vecino - costo_actual

            # Aceptar mejor solución o con probabilidad si es peor
            if delta < 0 or random.random() < math.exp(-delta / T):
                actual = vecino
                costo_actual = costo_vecino
                if costo_vecino < mejor_costo:
                    mejor = vecino
                    mejor_costo = costo_vecino

        historico.append(costo_actual)
        T *= alpha  # enfriamiento

    return mejor, mejor_costo, historico


def generar_vecino(solucion: TransportSolution):
    """
    Genera una nueva asignación cambiando una pequeña cantidad entre dos celdas distintas.
    No garantiza que cumpla restricciones; se repara luego.
    """
    asignacion = deepcopy(solucion.asignacion)
    filas, columnas = asignacion.shape

    i1, j1 = random.randint(0, filas - 1), random.randint(0, columnas - 1)
    i2, j2 = random.randint(0, filas - 1), random.randint(0, columnas - 1)

    while i1 == i2 and j1 == j2:
        i2, j2 = random.randint(0, filas - 1), random.randint(0, columnas - 1)

    delta = random.randint(1, 10)

    if asignacion[i1][j1] >= delta:
        asignacion[i1][j1] -= delta
        asignacion[i2][j2] += delta

    return TransportSolution(asignacion, solucion.problem)
