from constants import END_AGE, NUM_ITERATIONS, INFLATION_RATE, SOCIAL_SECURITY_AGE
from market_model import get_random_market_return_rate
from config import Config
import matplotlib.pyplot as plt

class SimState:
    def __init__(
            self,
            start_age:int,
            start_balance_millions:float,
            retirement_costs:float,
            retirement_costs_age: int,
            social_security_monthly: float,
            plot_flag: bool,
        ):
        # constants
        self.start_age = start_age
        self.start_balance_millions = start_balance_millions
        self.retirement_costs = retirement_costs
        self.retirement_costs_age = retirement_costs_age
        self.social_security_monthly = social_security_monthly
        self.plot_flag = plot_flag
        # iteration variables
        self.it_age = None
        self.it_balance = None
        self.it_costs = None
        self.it_age_array = []
        self.it_balance_array = []
        # outputs
        self.it_end_balance = []
        if self.plot_flag:
            plt.figure()

    def start_interation(self):
        self.it_age = self.start_age
        self.it_balance = self.start_balance_millions*1E6
        self.it_age_array = []
        self.it_balance_array = []
    
    def step_iteration(self):
        market_return_rate = get_random_market_return_rate()
        costs = self.get_retirement_costs(self.it_age)
        social_security = self.get_social_security_annual(self.it_age)
        market_return = (self.it_balance - costs/2) * market_return_rate
        self.it_balance += market_return + social_security - costs
        # increment
        self.it_age += 1
        if self.plot_flag:
            self.it_age_array.append(self.it_age)
            self.it_balance_array.append(self.it_balance)
    
    def end_iteration(self):
        self.it_end_balance.append(self.it_balance)
        plt.plot(self.it_age_array,self.it_balance_array)

    def get_retirement_costs(self,age):
        if age < self.retirement_costs_age:
            raise Exception(f"{age} less than {self.retirement_costs_age}")
        return(self.retirement_costs*(1 + INFLATION_RATE)**(age - self.retirement_costs_age))

    def get_social_security_annual(self,age):
        return(self.social_security_monthly*12 if age >= SOCIAL_SECURITY_AGE else 0)

    def get_risk(self):
        return(len(list(filter(lambda x: x < 0,self.it_end_balance)))/len(self.it_end_balance))
    
    def results(self):
        print("===INPUTS===")
        print(f"  Retirement Age: {self.start_age}")
        print(f"  Starting Balance: ${self.start_balance_millions}M")
        print(f"  Annual Retirement Costs @ Age {self.retirement_costs_age}: ${round(self.retirement_costs)}")
        print(f"  Inflation: {round(INFLATION_RATE*100,2)}%")
        print(f"  N Iterations: {NUM_ITERATIONS}")
        print("===OUTPUTS===")
        print(f"  Risk: {int(round(self.get_risk()*100,0))}%")
        if self.plot_flag:
            plt.title("FIRE Sims")
            plt.grid()
            plt.xlabel("Age [yr]")
            plt.ylabel("Balance [$]")
            # plt.ylim(0,9E6)
            plt.show()
    

sim_state = SimState(
    Config.start_age,
    Config.start_balance_millions,
    Config.retirement_costs,
    Config.retirement_costs_age,
    Config.social_security_monthly,
    Config.plot_flag,
)
for iteration in range(NUM_ITERATIONS):
    sim_state.start_interation()
    while sim_state.it_age < END_AGE:
        sim_state.step_iteration()
    sim_state.end_iteration()

sim_state.results()