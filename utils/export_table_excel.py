import pandas as pd
import os

def exportar_resultados_excel(nombre_archivo: str, resultados: list):
    """
    Exporta los resultados de los algoritmos a un archivo Excel.
    
    :param nombre_archivo: nombre del archivo Excel (ej: resultados.xlsx)
    :param resultados: lista de diccionarios con claves: Algoritmo, Costo, EsValido
    """
    df = pd.DataFrame(resultados)
    
    carpeta = "resultados_excel"
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, nombre_archivo)
    
    df.to_excel(ruta, index=False)
