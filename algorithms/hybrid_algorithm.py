import random
import math
from models.solution import TransportSolution
from utils.repair import reparar_asignacion

def hybrid_sa_tabu(sol_inicial: TransportSolution, T_inicial=1000, T_final=1e-3, alfa=0.85, L=20, tamaño_tabu=10, num_vecinos=4):
    # Paso 1: Inicializar S_actual
    actual = sol_inicial.clone()

    # Paso 2: Inicializar S_asp ← S_actual
    mejor = sol_inicial.clone()

    # Paso 3: Inicializar lista tabú vacía
    lista_tabu = []

    historico_costo = []
    historico_mejor = []

    # Paso 4: Inicializar temperatura
    niveles_temperatura = int(math.log(T_final / T_inicial) / math.log(alfa)) + 1
    T = T_inicial

    # Paso 5: Repetir mientras T > T_final (loop externo de temperaturas)
    for _ in range(niveles_temperatura):
        # Paso 6: Repetir L veces por cada temperatura (loop interno)
        for _ in range(L):
            # Paso 7: Generar N vecinos de la solución actual
            vecinos = generar_vecinos(actual, num_vecinos)

            # Paso 8: Reparar todos los vecinos y filtrar válidos
            vecinos_reparados = [(reparar_asignacion(v), m) for v, m in vecinos]
            vecinos_validos = [(v, m) for v, m in vecinos_reparados if v.is_valid()]

            if not vecinos_validos:
                continue

            # Paso 9: Escoger el mejor vecino (menor costo)
            mejor_vecino, movimiento = min(vecinos_validos, key=lambda x: x[0].costo_total())

            # Paso 10: Evaluar si el movimiento no está en la lista tabú
            if movimiento not in lista_tabu:
                delta = mejor_vecino.costo_total() - actual.costo_total()

                # Paso 11: Aceptación por criterio SA (mejora o probabilidad)
                if delta < 0:
                    actual = mejor_vecino
                    lista_tabu.insert(0, movimiento)
                    if len(lista_tabu) > tamaño_tabu:
                        lista_tabu.pop()
                elif random.random() < math.exp(-delta / T):
                    actual = mejor_vecino
                    lista_tabu.insert(0, movimiento)
                    if len(lista_tabu) > tamaño_tabu:
                        lista_tabu.pop()

                # Paso 12: Actualizar mejor solución S_asp si mejora
                if actual.costo_total() < mejor.costo_total():
                    mejor = actual.clone()

            # Paso 13: Si el movimiento es tabú pero mejora la mejor solución → criterio de aspiración
            elif mejor_vecino.costo_total() < actual.costo_total():
                actual = mejor_vecino
                lista_tabu.insert(0, movimiento)
                if len(lista_tabu) > tamaño_tabu:
                    lista_tabu.pop()
                mejor = actual.clone()

        # Paso 14: Reducir la temperatura
        T *= alfa

        # Paso 15: Registrar historial
        historico_costo.append(actual.costo_total())
        historico_mejor.append(mejor.costo_total())

    return mejor, mejor.costo_total(), historico_costo, historico_mejor


def generar_vecinos(solucion: TransportSolution, cantidad: int):
    vecinos = []
    for _ in range(cantidad):
        asignacion = solucion.asignacion.copy()
        filas, columnas = asignacion.shape
        i1, j1 = random.randint(0, filas - 1), random.randint(0, columnas - 1)
        i2, j2 = random.randint(0, filas - 1), random.randint(0, columnas - 1)

        while i1 == i2 and j1 == j2:
            i2, j2 = random.randint(0, filas - 1), random.randint(0, columnas - 1)

        delta = random.randint(1, 25)

        if asignacion[i1][j1] >= delta:
            asignacion[i1][j1] -= delta
            asignacion[i2][j2] += delta

        vecino = TransportSolution(asignacion, solucion.problem)
        movimiento = (i1, j1, i2, j2)
        vecinos.append((vecino, movimiento))
    return vecinos