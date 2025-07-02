import numpy as np
from models.solution import TransportSolution

def reparar_asignacion(solucion: TransportSolution) -> TransportSolution:
    """
    Ajusta una asignación para que cumpla con las restricciones de oferta (supply) y demanda (demand).
    Si una fila o columna se pasa, reduce desde las celdas de mayor valor.
    Si falta, intenta completarla desde filas con oferta disponible.
    """

    asignacion = np.copy(solucion.asignacion)
    costos = solucion.problem.costos
    supply = solucion.problem.supply
    demand = solucion.problem.demand
    filas, columnas = asignacion.shape

    # Ajustar columnas (demandas)
    for j in range(columnas):
        total_col = asignacion[:, j].sum()
        if total_col > demand[j]:
            # Reducir exceso desde las filas más costosas
            exceso = total_col - demand[j]
            filas_ordenadas = np.argsort(-costos[:, j])
            for i in filas_ordenadas:
                reducible = min(exceso, asignacion[i, j])
                asignacion[i, j] -= reducible
                exceso -= reducible
                if exceso <= 0:
                    break

        elif total_col < demand[j]:
            # Aumentar desde las filas más baratas
            deficit = demand[j] - total_col
            filas_ordenadas = np.argsort(costos[:, j])
            for i in filas_ordenadas:
                disponible = supply[i] - asignacion[i].sum()
                cantidad = min(deficit, disponible)
                asignacion[i, j] += cantidad
                deficit -= cantidad
                if deficit <= 0:
                    break

    return TransportSolution(asignacion, solucion.problem)
