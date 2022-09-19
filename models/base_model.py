import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import solve_ivp


class BaseModel:

    def __init__(self, initial_params, initial_population_size, tf):
        assert len(initial_params) == 4
        self.tf = tf
        self.initial_susceptible, self.initial_sick, self.initial_recovered, self.initial_immune = initial_params
        self.initial_params = initial_params
        self.initial_population_size = initial_population_size

    def diff_equations(self, generation, population_curves):
        raise NotImplemented

    def solve(self):
        solution = solve_ivp(fun=self.diff_equations, y0=self.initial_params, t_span=(0, self.tf))
        self.evaluated_times = solution.ts
        self.y = solution.y
        print(self.y)
        # self.susceptible = s
        # self.infectious = inf
        # self.removed = r
        # self.inmmune = i
        # return s, inf, r, i

    def plotdata(self):
        # plot the data
        fig = plt.figure(figsize=(12, 6))
        ax = [fig.add_subplot(221, axisbelow=True),
              fig.add_subplot(223),
              fig.add_subplot(122)]

        ax[0].plot(self.evaluated_times, self.susceptible, lw=4, label='Fraction Susceptible')
        ax[0].plot(self.generations, self.infectious, lw=4, label='Fraction Infective')
        ax[0].plot(self.generations, self.removed, lw=4, label='Recovered')
        ax[0].plot(self.generations, 1-self.susceptible-self.infectious-self.removed, lw=4, label='Inmmune')
        ax[0].set_title('Susceptible, Infectious and Recovered Populations')
        ax[0].set_xlabel('Time /days')
        ax[0].set_ylabel('Fraction')

        ax[1].plot(self.generations, self.infectious, lw=3, label='Infective')
        ax[1].set_title('Infectious Population')
        # if e is not None: ax[1].plot(generations, e, lw=3, label='Exposed')
        ax[1].set_ylim(0, 0.3)
        ax[1].set_xlabel('Time /days')
        ax[1].set_ylabel('Fraction')

        ax[2].plot(self.susceptible, self.infectious, lw=3, label='s, i trajectory')
        ax[2].plot([1 / self.R0, 1 / self.R0], [0, 1], '--', lw=3, label='di/dt = 0')
        ax[2].plot(self.susceptible[0], self.infectious[0], '.', ms=20, label='Initial Condition')
        ax[2].plot(self.susceptible[-1], self.infectious[-1], '.', ms=20, label='Final Condition')
        ax[2].set_title('State Trajectory')
        ax[2].set_aspect('equal')
        ax[2].set_ylim(0, 1.05)
        ax[2].set_xlim(0, 1.05)
        ax[2].set_xlabel('Susceptible')
        ax[2].set_ylabel('Infectious')

        for a in ax:
            a.grid(True)
            a.legend()

        plt.tight_layout()

    def estimate_parameters(self, *args, **kwargs):
        raise NotImplementedError

    def loss(self, *true_population_curves):
        loss = 0
        for predicted_curve, true_curve in zip([self.susceptible, self.infectious, self.removed, self.inmmune], true_population_curves):
            loss += sum((predicted_curve-true_curve)**2)
        return loss
