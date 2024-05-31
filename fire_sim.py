from constants import END_AGE, NUM_ITERATIONS, BONDS_AVERAGE_RETURNS_RATE, INFLATION_RATE
from market_model import get_random_market_return_rate
from config import Config
import matplotlib.pyplot as plt
import numpy as np
from utils import convert_to_millions_string, convert_to_thousands_string

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
        self.it_average_market_return_array = []
        self.it_end_balance_array = []
        self.it_age_zero_balance_array = []
        if self.config.get_plot_flag():
            plt.figure()

    def start_interation(self):
        self.it_age = self.config.get_retirement_start_age()
        self.it_age_zero_balance = END_AGE
        self.it_prev_market_return_rate = 0.0
        self.it_balance = self.config.get_retirement_start_balance()
        self.it_age_array = [self.it_age]
        self.it_balance_array = [self.it_balance]
        self.it_market_return_array = []
    
    def step_iteration(self):
        market_return_rate = get_random_market_return_rate()
        bonds_fraction = self.config.get_retirement_balance_bonds_fraction(self.it_age)
        costs = self.config.get_retirement_costs(
            inf_adj=True,
            age=self.it_age,
            previous_year_market_return_rate=self.it_prev_market_return_rate,
        )
        # apply costs (conservatively assumes costs applied before returns)
        self.it_balance += -costs
        # calculate returns
        bonds_return = self.it_balance*bonds_fraction*BONDS_AVERAGE_RETURNS_RATE
        market_return = self.it_balance*(1-bonds_fraction)*market_return_rate
        social_security = self.config.get_social_security_annual(
            inf_adj=True,
            age=self.it_age,
        )
        # apply returns
        self.it_balance += bonds_return + market_return + social_security
        # save outputs
        if self.it_balance <= 0 and self.it_age < self.it_age_zero_balance:
            self.it_age_zero_balance = self.it_age
        self.it_prev_market_return_rate = market_return_rate
        self.it_market_return_array.append(market_return_rate)
        # increment
        self.it_age += 1
        if self.config.get_plot_flag():
            self.it_age_array.append(self.it_age)
            self.it_balance_array.append(self.it_balance)
    
    def end_iteration(self):
        self.it_end_balance_array.append(self.it_balance)
        self.it_age_zero_balance_array.append(self.it_age_zero_balance)
        self.it_average_market_return_array.append(np.average(self.it_market_return_array))
        plt.plot(self.it_age_array,self.it_balance_array)

    def get_risk(self):
        return(len(list(filter(lambda x: x <= 0,self.it_end_balance_array)))/len(self.it_end_balance_array))
    
    def get_average_zero_balance_age(self):
        return(np.average(self.it_age_zero_balance_array))
    
    def results(self):
        print()
        print("===INPUTS===")
        print(f"Retirement Start:")
        print(f"  Age: {self.config.get_retirement_start_age()}")
        print(f"  Balance: ${self.config.get_retirement_start_balance_m()}M")
        print(f"  Bonds Allocation: {int(round(self.config.get_retirement_balance_bonds_fraction(self.config.get_retirement_start_age())*100))}%")
        print(f"  Annual Living Costs (base): "+convert_to_thousands_string(int(round(self.config.get_retirement_costs(inf_adj=False,age=self.config.get_retirement_start_age(),previous_year_market_return_rate=100.0)))))
        print(f"  Annual Living Costs (inf. adj.): "+convert_to_thousands_string(int(round(self.config.get_retirement_costs(inf_adj=True,age=self.config.get_retirement_start_age(),previous_year_market_return_rate=100.0)))))  
        print(f"General:")
        print(f"  Average Market Returns: {round(np.average(self.it_average_market_return_array)*100,2)}%")
        print(f"  Average Bonds Returns: {round(BONDS_AVERAGE_RETURNS_RATE*100,2)}%")
        print(f"  Inflation: {round(INFLATION_RATE*100,2)}%")  
        print(f"  N Iterations: {NUM_ITERATIONS}")
        print("===OUTPUTS===")
        print(f"Retirement End:")
        print(f"  Age: {END_AGE}")
        print(f"  Balance (median): "+convert_to_millions_string(np.median(self.it_end_balance_array)))
        print(f"  Bonds Allocation: {int(round(self.config.get_retirement_balance_bonds_fraction(END_AGE)*100))}%")
        print(f"  Annual Living Costs (base): "+convert_to_thousands_string(int(round(self.config.get_retirement_costs(inf_adj=False,age=END_AGE,previous_year_market_return_rate=100.0)))))
        print(f"  Annual Living Costs (inf. adj.): "+convert_to_thousands_string(int(round(self.config.get_retirement_costs(inf_adj=True,age=END_AGE,previous_year_market_return_rate=100.0))))) 
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