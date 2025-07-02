import pandas as pd
import os

def exportar_historico_costos(nombre_archivo: str, historicos: dict):
    """
    Exporta los historiales de costos de varios algoritmos a un archivo Excel o CSV,
    rellenando con None si las listas tienen diferentes longitudes.
    """
    # Calcular la longitud máxima entre todas las listas
    max_len = max(len(lista) for lista in historicos.values())

    # Rellenar con None hasta igualar longitudes
    datos_normalizados = {
        nombre: lista + [None] * (max_len - len(lista))
        for nombre, lista in historicos.items()
    }

    df = pd.DataFrame(datos_normalizados)

    carpeta = "resultados_excel"
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, nombre_archivo)

    if nombre_archivo.endswith(".csv"):
        df.to_csv(ruta, index=False)
    else:
        df.to_excel(ruta, index=False)
