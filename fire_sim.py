from constants import END_AGE, NUM_ITERATIONS, SOCIAL_SECURITY_AGE, INFLATION_RATE
from market_model import get_random_market_return_rate
from config import Config
import matplotlib.pyplot as plt
import numpy as np

class SimState:
    def __init__(
            self,
            config: Config,
        ):
        # config (inputs)
        self.config = config
        # initiailize iteration variables
        self.start_interation()
        # outputs
        self.it_end_balance_array = []
        self.it_age_zero_balance_array = []
        if self.config.get_plot_flag():
            plt.figure()

    def start_interation(self):
        self.it_age = self.config.get_retirement_start_age()
        self.it_age_zero_balance = END_AGE
        self.it_prev_market_return_rate = 0.0
        self.it_balance = self.config.get_retirement_start_balance()
        self.it_age_array = []
        self.it_balance_array = []
    
    def step_iteration(self):
        market_return_rate = get_random_market_return_rate()
        costs = self.config.get_retirement_costs_inflation_adjusted(self.it_age,self.it_prev_market_return_rate)
        social_security = self.config.get_social_security_annual_inflation_adjusted(self.it_age)
        market_return = (self.it_balance - costs/2) * market_return_rate # average market balance
        self.it_balance += market_return + social_security - costs
        # save outputs
        if self.it_balance <= 0 and self.it_age < self.it_age_zero_balance:
            self.it_age_zero_balance = self.it_age
        # increment
        self.it_age += 1
        self.it_prev_market_return_rate = market_return
        if self.config.get_plot_flag():
            self.it_age_array.append(self.it_age)
            self.it_balance_array.append(self.it_balance)
    
    def end_iteration(self):
        self.it_end_balance_array.append(self.it_balance)
        self.it_age_zero_balance_array.append(self.it_age_zero_balance)
        plt.plot(self.it_age_array,self.it_balance_array)

    def get_risk(self):
        return(len(list(filter(lambda x: x <= 0,self.it_end_balance_array)))/len(self.it_end_balance_array))
    
    def get_average_zero_balance_age(self):
        return(np.average(self.it_age_zero_balance_array))
    
    def results(self):
        print("===INPUTS===")
        print(f"  Retirement Age: {self.config.get_retirement_start_age()}")
        print(f"  Starting Balance: ${self.config.get_retirement_start_balance_m()}M")
        print(f"  Inflation: {round(INFLATION_RATE*100,2)}%")
        print(f"  N Iterations: {NUM_ITERATIONS}")
        print("===OUTPUTS===")
        print(f"  Risk: {int(round(self.get_risk()*100,0))}%")
        print(f"  Average Age of Zero Balance: {int(round(self.get_average_zero_balance_age(),0))}")
        if self.config.get_plot_flag():
            plt.title("FIRE Sims")
            plt.grid()
            plt.xlabel("Age [yr]")
            plt.ylabel("Balance [$]")
            plt.show()
    
config = Config()
sim_state = SimState(config)
for iteration in range(NUM_ITERATIONS):
    sim_state.start_interation()
    while sim_state.it_age < END_AGE:
        sim_state.step_iteration()
    sim_state.end_iteration()

sim_state.results()