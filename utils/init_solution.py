import numpy as np

def generar_solucion_menor_costo(costos, supply, demand):
    filas, columnas = costos.shape
    oferta = supply.copy()
    demanda = demand.copy()
    asignacion = np.zeros_like(costos)

    # Ordenar las celdas por costo ascendente
    celdas = sorted(
        [(i, j) for i in range(filas) for j in range(columnas)],
        key=lambda x: costos[x[0]][x[1]]
    )

    for i, j in celdas:
        cantidad = min(oferta[i], demanda[j])
        if cantidad > 0:
            asignacion[i][j] = cantidad
            oferta[i] -= cantidad
            demanda[j] -= cantidad

    return asignacion
