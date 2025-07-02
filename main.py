from models.problem import TransportProblem
from models.solution import TransportSolution
from utils.init_solution import generar_solucion_menor_costo
from utils.export_table_excel import exportar_resultados_excel
from utils.export_history_excel import exportar_historico_costos
from algorithms.simulated_annealing import simulated_annealing
from algorithms.tabu_search import tabu_search
from algorithms.hybrid_algorithm import hybrid_sa_tabu
from utils.plot import graficar_costo_y_nivasp, graficar_costo, generar_grafica_comparativa_convergencia
import numpy as np

# ---------------------
# Datos del problema
# ---------------------
costos = [
    [5, 1, 2, 3, 4, 7],
    [7, 2, 3, 1, 5, 6],
    [9, 1, 9, 5, 2, 3],
    [6, 5, 8, 4, 1, 4],
    [8, 7,11, 6, 4, 5],
    [2, 5, 7, 5, 2, 1]
]
supply = [400, 500, 300, 150, 600, 350]
demand = [300, 500, 700, 300, 250, 250]

# ---------------------
# Inicializar problema y solución base
# ---------------------
problem = TransportProblem(costos, supply, demand)
asignacion = generar_solucion_menor_costo(problem.costos, problem.supply, problem.demand)
sol_inicial = TransportSolution(asignacion, problem)

print("Solución inicial:")
print(sol_inicial)
print("¿Válida?", sol_inicial.is_valid())

# ---------------------
# Ejecutar Simulated Annealing
# ---------------------
EJECUTAR_SA = True

if EJECUTAR_SA:
    mejor_sa, costo_sa, historico_sa = simulated_annealing(sol_inicial)
    print("\nSIMULATED ANNEALING:")
    print("Costo final:", costo_sa)
    print("¿Solución válida?", mejor_sa.is_valid())
    print(mejor_sa)
    graficar_costo("Comportamiento del costo con algoritmo Recocido simulado (simulated annealing)",historico_sa, "resultados/grafico_simulated_annealing.png")

# ---------------------
# Ejecutar Tabu Search
# ---------------------
EJECUTAR_TS = True

if EJECUTAR_TS:
    mejor_ts, costo_ts, historico_ts, historico_nivasp, historial_listas_tabu = tabu_search(sol_inicial)
    print("\nTABU SEARCH:")
    print("Costo final:", costo_ts)
    print("¿Solución válida?", mejor_ts.is_valid())
    print(mejor_ts)
    graficar_costo_y_nivasp("Comportamiento del costo con algoritmo búsqueda tabú (tabu search)",historico_ts, historico_nivasp, "resultados/grafico_tabu.png")

# ---------------------
# Ejecutar Algoritmo Híbrido
# ---------------------
EJECUTAR_HIBRIDO = True

if EJECUTAR_HIBRIDO:
    mejor_h, costo_h, historico_h, historico_mejor_h = hybrid_sa_tabu(sol_inicial)
    print("\nHÍBRIDO SA + TABU SEARCH:")
    print("Costo final:", costo_h)
    print("¿Solución válida?", mejor_h.is_valid())
    print(mejor_h)
    graficar_costo_y_nivasp("Comportamiento del costo con algoritmo híbrido (simulated annealing + tabu search)", historico_h, historico_mejor_h, "resultados/grafico_hibrido.png")

if EJECUTAR_SA and EJECUTAR_TS and EJECUTAR_HIBRIDO:
    generar_grafica_comparativa_convergencia(historico_sa, historico_ts, historico_h, "resultados/grafico_comparativo_convergencia.png")
resultados = [
    {"Algoritmo": "Solución Inicial", "Costo": sol_inicial.costo_total(), "EsValido": sol_inicial.is_valid()},
    {"Algoritmo": "Simulated Annealing", "Costo": costo_sa, "EsValido": mejor_sa.is_valid()},
    {"Algoritmo": "Tabu Search", "Costo": costo_ts, "EsValido": mejor_ts.is_valid()},
    {"Algoritmo": "Híbrido SA + Tabu", "Costo": costo_h, "EsValido": mejor_h.is_valid()},
]

exportar_resultados_excel("resumen_resultados.xlsx", resultados)

exportar_historico_costos(
    "historico_costos.xlsx",
    {
        "Simulated Annealing": historico_sa,
        "Tabu Search": historico_ts,
        "Híbrido SA + Tabu": historico_h
    }
)