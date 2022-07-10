class SIRModel:

    def __init__(self, initial_susceptible, initial_sick, initial_recovered, initial_population_size):
        self.initial_susceptible = initial_susceptible
        self.initial_sick = initial_sick
        self.initial_recovered = initial_recovered
        self.generation = 0
        self.initial_population_size = initial_population_size
