import numpy as np

from models.base_model import BaseModel


class SIR(BaseModel):
    def __init__(self, initial_params, initial_population_size, generations):
        assert len(initial_params) == 3
        extended_initial_params = initial_params + (0, )
        super().__init__(extended_initial_params, initial_population_size, generations)

    # From https://colab.research.google.com/github/jckantor/CBE30338/blob/master/docs/03.09-COVID-19.ipynb
    def diff_equations(self, generation, population_curves):
        s, inf, r, inm = population_curves
        dsdt = -self.beta * s * inf
        didt = self.beta * s * inf - self.gamma * inf
        drdt = self.gamma * inf
        dinmdt = 0
        return [dsdt, didt, drdt, dinmdt]

    def estimate_parameters_from_R0(self, t_infectious, R0):
        self.beta = 1/t_infectious
        self.gamma = self.beta/R0
        self.R0 = R0

    def estimate_parameters_from_periods(self, t_infectious, t_recovery):
        self.beta = 1/t_infectious
        self.gamma = 1/t_recovery
        self.R0 = self.beta/self.gamma
