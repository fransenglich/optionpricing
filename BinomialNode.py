import math
import numpy as np


# Underlying asset moves by factor u or d:
#   u >= 1
#   0 < d <= 1
#
# S is underlying price.
#
# The price in the next period is either:
#   S_up = S * u
#   S_down = S * d
#
# Further:
#   u = e^(sigma * sqrt(delta t))
#   d = 1 / d
#
# The leaves has the value of the intrinsic value:
#   Call option: max(S_n - K, 0)
#   Put option: max(K - S_n, 0)
#
# K is the option's strike price, S_n is spot price of asset at period n. S_0
# is the initial intrinsic value.
#
# The tree is recombinant, reducing the number of nodes.

class BinomialNode:
    """
    A node in a binomial tree for option pricing.

    It has the public variable stockvalue, and the central member function
    option_price().

    See the test cases in class TestBinomialNode.

    Some of the material used:

    * Options, Futures and Other Derivatives. John C. Hull (2022)
    * https://www.youtube.com/watch?v=AukJ1gDeErw
    * https://www.youtube.com/watch?v=eA5AtTx3rRI
    * https://www.youtube.com/watch?v=PZrmOh2nZus
    """

    stockvalue: float = None

    __name: str
    __strikeprice: float = None
    __upnode = None
    __downnode = None

    # The discount rate
    __r = 0.0

    # Whether to compound continously or discretely
    __discrete: bool

    # t
    __T: float

    def __init__(self, name: str, stockvalue: float, strikeprice: float,
                 r: float, upnode, downnode, compound="discretely",
                 T: float = 1):
        """An init function with some checks."""

        self.__name = name
        self.stockvalue = stockvalue
        self.__strikeprice = strikeprice

        assert r >= 0 and r < 1
        self.__r = r

        if compound == "discretely":
            self.__discrete = True
        elif compound == "continously":
            self.__discrete = False
        else:
            raise ValueError("Wrong value for argument 'compound'.")

        assert (downnode is None) == (upnode is None), \
               "Both children should be None or both set."
        self.__upnode = upnode
        self.__downnode = downnode

        self.__T = T

    def option_price(self) -> float:
        """Returns the option price for the state this node represent in an
        binomial tree."""

        if not self.__upnode:
            # We're a leaf.

            # (We for now assume we're a call option.)
            # We know our value because the stock value and strike price is
            # known.
            option_price = max(self.stockvalue - self.__strikeprice, 0)
            print(f"{self.__name}: "
                  "Leaf, returning option value {option_price}.")
            return option_price

        call_up = self.__upnode.option_price()
        call_down = self.__downnode.option_price()

        # The amount of shares for our riskless portfolio
        amount = (call_up - call_down) / (self.__upnode.stockvalue -
                                          self.__downnode.stockvalue)
        print(f"{self.__name}: The stock amount is {amount}.")

        # The equation for the portfolio value is:
        #   V = amount * stockvalue - option
        # We can choose both call_up or call_down
        V = amount * self.__upnode.stockvalue - call_up
        print(f"{self.__name}: Portfolio value is {V}.")

        if self.__discrete:
            PV = V / (1 + self.__r)
        else:
            PV = V * math.exp(-self.__r * self.__T)

        # The amount of the stock value
        owned_stockvalue = amount * self.stockvalue

        call_value = owned_stockvalue - PV
        print(f"{self.__name}: The option value is {call_value}.")

        return call_value


class MCBinomonialNode:
    """Implements option price using a Monte Carlo method.

    Wikipedia has good content on this:
    - https://en.wikipedia.org/wiki/Monte_Carlo_methods_for_option_pricing
    - https://en.wikipedia.org/wiki/Rational_pricing#Risk_neutral_valuation
    - https://en.wikipedia.org/wiki/Brownian_motion
    """

    def S(self, S_prev) -> float:
        """Computes a stock price by drawing from a random normal distribution,
        while assuming a geometric Brownian motion.
        """

        mu = 0.4  # Constant drift, expected rate of return
        sigma = 0.3  # Volatility, SD, assumed constant
        M = 10_000  # Number of simulations
        # S_0 = 30  # Initial stock value # TODO set
        t = 1  # TODO

        # Z ~ N(0, 1)
        Z = np.random.randm(M)

        # For one step, not path
        S = S_prev * np.exp((mu - 0.5 * sigma ** 2) * t +
                            sigma * np.sqrt(t) * Z)

        return S


def __generate_price_path(S0: float,
                          mu: float,
                          sigma: float,
                          t: float):
    """Generates and returns our sequence of stock returns, according to a
    simulated geometric Brownian motion."""

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
                   r: float) -> float):
    S0 = 100.0
    mu = 0.05
    sigma = 0.2
    t = 1.0
    r = 0.04

    strike_price = 120
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


def main():
    test()


main()
