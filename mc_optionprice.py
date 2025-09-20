import numpy as np


def __generate_price_path(S0: float,
                          mu: float,
                          sigma: float,
                          t: float):
    """Generates and returns our sequence of stock returns, according to a
    simulated geometric Brownian motion.

    Private helper function."""

    N = 252
    dt = t / N

    S = np.empty(N + 1)
    S[0] = S0

    for i in range(N):
        Z = np.random.normal()
        S[i + 1] = S[i] * np.exp((mu - 0.5 * sigma ** 2) *
                                 dt + sigma * np.sqrt(dt)*Z)

    return S


def mc_optionprice(S0: float,
                   mu: float,
                   sigma: float,
                   t: float,
                   r: float,
                   strike_price: float) -> float:
    """Implements option price using a Monte Carlo method.

    Assumes it's a call option.

    Arguments:
    - S0: initial stock price
    - mu: Constant drift, expected rate of return
    - sigma: Volatility, SD, assumed constant
    - t: TODO
    - r: risk-free discount rate
    - strike_price: the option's strike price

    Wikipedia has good content on this:
    - https://en.wikipedia.org/wiki/Monte_Carlo_methods_for_option_pricing
    - https://en.wikipedia.org/wiki/Rational_pricing#Risk_neutral_valuation
    - https://en.wikipedia.org/wiki/Brownian_motion
    """

    N = 100
    C = np.empty(N)

    for i in range(N):
        path = __generate_price_path(S0, mu, sigma, t)
        S_last = path[-1]

        # We calculate the call's value:
        C[i] = max(S_last - strike_price, 0)

    avg = C.mean()
    discounted = avg * np.exp(r * t)

    return discounted
