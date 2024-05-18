# fire_sim
A simulation used for FIRE (Financial Independence Retire Early) planning.

Simulates an account balance post retirement by modeling the S&P 500 annual returns as a normal distribution fit to historical data.
The output `Risk` represents the number of iterations (simulation from retirement to death) for which the account balance ended negative (driven primarily by Sequence of Returns Risk).

To use the sim, simply add a `config.py` file which implements the following class:
```
class Config:
    start_age = 40 # retirement age
    start_balance_millions = 2.0 # millions of dollars
    retirement_costs = 100000 # annual retirement costs at retirement_costs_age (will be adjusted for inflation)
    retirement_costs_age = 35 # age that retirement_costs is valid
    social_security_monthly = 100
    plot_flag = False # plots sim iterations
```

![image](https://github.com/t-mccawley/fire_sim/assets/29646748/e60c1291-5226-46b7-86ab-75ac8c9d388e)
![image](https://github.com/t-mccawley/fire_sim/assets/29646748/b129cdc1-eb27-475d-a630-2e23f60e8634)
