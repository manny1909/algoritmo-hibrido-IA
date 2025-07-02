import numpy as np

class TransportProblem:
    def __init__(self, costos, supply, demand):
        self.costos = np.array(costos)
        self.supply = np.array(supply)
        self.demand = np.array(demand)

    def get_shape(self):
        return self.costos.shape
