import numpy as np
from copy import deepcopy

class TransportSolution:
    def __init__(self, asignacion, problem):
        self.asignacion = np.array(asignacion)
        self.problem = problem

    def costo_total(self):
        return np.sum(self.asignacion * self.problem.costos)

    def is_valid(self):
        supply_check = np.all(np.sum(self.asignacion, axis=1) == self.problem.supply)
        demand_check = np.all(np.sum(self.asignacion, axis=0) == self.problem.demand)
        non_negative_check = np.all(self.asignacion >= 0)

        return supply_check and demand_check and non_negative_check

    def clone(self):
        return TransportSolution(deepcopy(self.asignacion), self.problem)

    def __str__(self):
        return f"Asignación:\n{self.asignacion}\nCosto total: {self.costo_total()}"
