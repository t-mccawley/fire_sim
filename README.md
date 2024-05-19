# fire_sim
A simulation used for FIRE (Financial Independence Retire Early) planning.

Simulates an account balance post retirement by modeling the S&P 500 annual returns as a normal distribution fit to historical data.
The output `Risk` represents the number of iterations (simulation from retirement to death) for which the account balance ended negative (driven primarily by Sequence of Returns Risk).

To use the sim, simply implement a `Config(ConfigABC)` in `config.py` to store your input parameters and configurations.

Example output:

![image](https://github.com/t-mccawley/fire_sim/assets/29646748/cac48f36-3a1a-4a19-a785-c17687b984b6)
## Appendix
### Underlying S&P 500 returns data and probability model:
![image](https://github.com/t-mccawley/fire_sim/assets/29646748/e60c1291-5226-46b7-86ab-75ac8c9d388e)
![image](https://github.com/t-mccawley/fire_sim/assets/29646748/b129cdc1-eb27-475d-a630-2e23f60e8634)
