import matplotlib.pyplot as plt
import os

def graficar_costo(title, historico, output_path="resultados/grafico.png"):
    plt.figure(figsize=(10, 5))
    plt.plot(historico, marker='o', color='red', linestyle='-', linewidth=1, label="f(S_actual)")
    plt.xlabel("Iteración")
    plt.ylabel("Costo total")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.show()

def graficar_costo_y_nivasp(title, historico, nivasp, output_path="resultados/grafico_tabu_nivasp.png"):
    plt.figure(figsize=(10, 5))
    plt.plot(historico, label="f(S_actual)", color='blue', marker='o', linestyle='-')
    plt.plot(nivasp, label="nivasp (mejor encontrado)", color='green', linestyle='--', marker='x')
    plt.title(title)
    plt.xlabel("Iteración")
    plt.ylabel("Costo total")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.show()

def generar_grafica_comparativa_convergencia(historico_sa, historico_ts, historico_hibrido, output_path="resultados/grafico_comparativo_convergencia.png"):
    """
    Genera una gráfica de comparación de convergencia (históricos de costo) entre tres algoritmos.

    Args:
        historico_sa (list): Lista de costos del algoritmo Simulated Annealing.
        historico_ts (list): Lista de costos del algoritmo Tabu Search.
        historico_hibrido (list): Lista de costos del algoritmo híbrido.
        output_path (str): Ruta donde guardar la imagen generada.
    """

    plt.figure(figsize=(10, 6))
    plt.plot(historico_sa, label="Simulated Annealing")
    plt.plot(historico_ts, label="Búsqueda Tabú")
    plt.plot(historico_hibrido, label="Híbrido SA + Tabú")

    plt.xlabel("Iteraciones")
    plt.ylabel("Costo Total")
    plt.title("Comparación de Convergencia de Algoritmos")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.show()
