# fire_sim
A simulation used for FIRE (Financial Independence Retire Early) planning.

Simulates an account balance post retirement by modeling the S&P 500 annual returns as a normal distribution fit to historical data. Costs, bond returns, and other factors are configurable and modeled as well.
The output `Risk` represents the number of iterations (simulation from retirement to death) for which the account balance ended negative (driven primarily by Sequence of Returns Risk).

To use the sim, simply implement a `Config(ConfigABC)` in `config.py` to store your input parameters and configurations. The config supports custom logic for retirement costs (spend less when market is down or as you get older) as well as custom logic for fraction of portfolio allocated to bonds.

Example outputs:

![image](https://github.com/t-mccawley/fire_sim/assets/29646748/3a514e11-d94f-43ff-98e9-bb36c959e190)
![image](https://github.com/t-mccawley/fire_sim/assets/29646748/32967098-9ec3-48e2-9fcb-12c1c98bc601)

## Appendix
### Underlying S&P 500 returns data and probability model:
![image](https://github.com/t-mccawley/fire_sim/assets/29646748/e60c1291-5226-46b7-86ab-75ac8c9d388e)
![image](https://github.com/t-mccawley/fire_sim/assets/29646748/b129cdc1-eb27-475d-a630-2e23f60e8634)
