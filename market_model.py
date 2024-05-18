from constants import RNG

def get_random_market_return_rate():
    # returns a random sample annual return rate from the market model for S&P 500
    # data from https://tradethatswing.com/average-historical-stock-market-returns-for-sp-500-5-year-up-to-150-year-averages/#:~:text=The%20average%20yearly%20return%20of%20the%20S%26P%20500%20is%2010.47,including%20dividends)%20is%207.74%25.
    # assume normal distribution
    MARKET_AVERAGE = 0.07864
    MARKET_STD_DEV = 0.19151
    return(RNG.normal(loc=MARKET_AVERAGE,scale=MARKET_STD_DEV))
