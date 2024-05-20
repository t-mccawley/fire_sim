from constants import INFLATION_RATE, SOCIAL_SECURITY_AGE
from abc import ABC, abstractmethod

def inflation_adjustment(initial_amount: float,time_period: float) -> float:
    if time_period < 0:
        raise Exception(f"{time_period} less than 0")
    return(initial_amount*(1 + INFLATION_RATE)**time_period)

def convert_to_millions_string(value:float) -> str:
    return(f"${round(value/1E6,1)}M")

def convert_to_thousands_string(value:float) -> str:
    return(f"${int(round(value/1E3,0))}k")

class ConfigABC(ABC):
    @abstractmethod
    def get_retirement_start_age(self) -> int:
        """Returns the age at start of retirement"""
        pass

    @abstractmethod
    def get_retirement_start_balance_m(self) -> float:
        """Returns the account balance (in millions of dollars) at start of retirement"""
        pass

    @abstractmethod
    def get_initial_social_secuirty_monthly(self) -> float:
        """Returns the initial social security amount (once social security begins)"""
        pass

    @abstractmethod
    def get_plot_flag(self) -> bool:
        """Returns a boolean indicating if visualization plots will be generated from the sim"""
        pass

    @abstractmethod
    def get_baseline_retirement_costs_age(self) -> int:
        """Returns an age for which the retirement costs are baselined for inflation (inflation adjustments will be computed from this age)"""
        pass

    @abstractmethod
    def get_baseline_retirement_costs(self,previous_year_market_return_rate:float,age:int) -> float:
        """Returns the annual retirement costs for a given baseline (get_baseline_retirement_costs_age)"""
        pass

    @abstractmethod
    def get_retirement_balance_bonds_fraction(self) -> float:
        """Returns the fraction of retirement balance that is invested in bonds"""

    def get_retirement_start_balance(self) -> float:
        """Returns the starting retirmenet balance"""
        return(self.get_retirement_start_balance_m()*1E6)
    
    def get_retirement_costs(self,inf_adj: bool,age:int,previous_year_market_return_rate:float) -> float:
        """Returns the annual retirement costs after inflation adjustment"""
        if age < self.get_baseline_retirement_costs_age():
            raise Exception(f"{age} less than {self.get_baseline_retirement_costs_age()}")
        initial_amount = self.get_baseline_retirement_costs(previous_year_market_return_rate,age)
        time_period = age - self.get_baseline_retirement_costs_age() if inf_adj else 0
        return(inflation_adjustment(initial_amount,time_period))
    
    def get_social_security_annual(self,inf_adj: bool,age:int) -> float:
        """Returns the annual social security benefit after inflation adjustment"""
        if age < SOCIAL_SECURITY_AGE:
            # No SS benefit yet
            return(0)
        initial_amount = 12.0*self.get_initial_social_secuirty_monthly()
        time_period = age - SOCIAL_SECURITY_AGE if inf_adj else 0
        return(inflation_adjustment(initial_amount,time_period))