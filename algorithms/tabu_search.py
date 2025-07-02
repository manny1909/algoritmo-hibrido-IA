import random
import numpy as np
from copy import deepcopy
from models.solution import TransportSolution
from utils.repair import reparar_asignacion

def tabu_search(sol_inicial: TransportSolution, iteraciones=100, tamaño_tabu=10):
    actual = sol_inicial.clone()
    mejor = sol_inicial.clone()

    lista_tabu = []
    historico_costo = []
    historico_mejor = []
    historial_listas_tabu = []

    for _ in range(iteraciones):
        vecinos = []
        movimientos = []

        for _ in range(30):
            vecino, movimiento = generar_vecino(actual)
            if movimiento in lista_tabu:
                continue

            vecino = reparar_asignacion(vecino)  # puedes comentar esta línea si no quieres reparar

            if vecino.is_valid():
                vecinos.append(vecino)
                movimientos.append(movimiento)

        if not vecinos:
            historico_costo.append(actual.costo_total())
            historico_mejor.append(mejor.costo_total())
            historial_listas_tabu.append(lista_tabu.copy())
            continue

        idx_mejor_vecino = seleccionar_mejor(vecinos)
        mejor_vecino = vecinos[idx_mejor_vecino]
        mejor_mov = movimientos[idx_mejor_vecino]

        if mejor_mov not in lista_tabu:
            actual = mejor_vecino
            lista_tabu.insert(0, mejor_mov)
            if len(lista_tabu) > tamaño_tabu:
                lista_tabu.pop()

            if actual.costo_total() < mejor.costo_total():
                mejor = actual.clone()

        historico_costo.append(actual.costo_total())
        historico_mejor.append(mejor.costo_total())
        historial_listas_tabu.append(lista_tabu.copy())  # se guarda copia de lista actual

    return mejor, mejor.costo_total(), historico_costo, historico_mejor, historial_listas_tabu

def generar_vecino(solucion: TransportSolution):
    asignacion = solucion.asignacion.copy()
    filas, columnas = asignacion.shape

    i1, j1 = random.randint(0, filas - 1), random.randint(0, columnas - 1)
    i2, j2 = random.randint(0, filas - 1), random.randint(0, columnas - 1)
    while (i1 == i2 and j1 == j2):
        i2, j2 = random.randint(0, filas - 1), random.randint(0, columnas - 1)

    delta = random.randint(5, 25)
    if asignacion[i1][j1] >= delta:
        asignacion[i1][j1] -= delta
        asignacion[i2][j2] += delta

    vecino = TransportSolution(asignacion, solucion.problem)
    movimiento = (i1, j1, i2, j2)
    return vecino, movimiento

def seleccionar_mejor(vecinos):
    costos = [v.costo_total() for v in vecinos]
    return costos.index(min(costos))
