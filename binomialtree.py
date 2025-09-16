import math


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
#
# You need to take into account discounting

class BinomialNode:
    """
    A node in a binomial tree for option pricing.

    It has the public variable stockvalue, and the central member function
    option_price().

    It has been verified for two time periods, t=0 and t=1.

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

    # T
    __T: float

    def __init__(self, name: str, stockvalue: float, strikeprice: float,
                 r: float, upnode, downnode, compound="discretely",
                 T: float = 1):
        """A vanilla init function."""

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


def main() -> None:
    print("----------- Call option, one step. --------------")

    # Let's run on the example in:
    # https://www.youtube.com/watch?v=AukJ1gDeErw

    # 1. We build the tree and specify our data/nodes.
    nu = BinomialNode("U",
                      stockvalue=48,
                      strikeprice=38,
                      r=0.05,
                      upnode=None,
                      downnode=None)
    nd = BinomialNode("D",
                      stockvalue=30,
                      strikeprice=38,
                      r=0.05,
                      upnode=None,
                      downnode=None)
    np = BinomialNode("P",
                      stockvalue=40,
                      strikeprice=38,
                      r=0.05,
                      upnode=nu,
                      downnode=nd)

    # The correct values should be:
    # up state: option value 10, stock value 48
    # down state: option value 0, stock value 30
    # stock amount: 10/18 = 0.55
    # option price: 6.35

    # 2. We compute our result
    ytprice = np.option_price()

    # The computed values matches the example on Youtube.
    print(f"Option price for Youtube-example: {ytprice}")

    print("----------- Call option, one step Hull fig. 13.1. --------------")
    hull_nu = BinomialNode("U",
                           stockvalue=22,
                           strikeprice=21,
                           r=0.04,
                           upnode=None,
                           downnode=None,
                           compound="continously",
                           T=0.25)
    hull_nd = BinomialNode("D",
                           stockvalue=18,
                           strikeprice=21,
                           r=0.04,
                           upnode=None,
                           downnode=None,
                           compound="continously",
                           T=0.25)
    hull_np = BinomialNode("P",
                           stockvalue=20,
                           strikeprice=21,
                           r=0.04,
                           upnode=hull_nu,
                           downnode=hull_nd,
                           compound="continously",
                           T=0.25)

    hull_price = hull_np.option_price()
    print(f"Option price for Hull fig. 31.1: {hull_price}")
    # Our computed stock amount, portfolio value and option price
    # #matches Hull

    print("----------- Call option, two steps. --------------")
    # We run the example in Hull (2022) p. 295, figure 13.4.

    # 1. We build the tree and specify our data/nodes.
    # Note that node E has two parents, B and C.
    nD = BinomialNode("D",
                      stockvalue=24.2,
                      strikeprice=21,
                      r=0.04,
                      upnode=None,
                      downnode=None,
                      compound="continously")
    nE = BinomialNode("E",
                      stockvalue=19.8,
                      strikeprice=21,
                      r=0.04,
                      upnode=None,
                      downnode=None,
                      compound="continously")
    nF = BinomialNode("F",
                      stockvalue=16.2,
                      strikeprice=21,
                      r=0.04,
                      upnode=None,
                      downnode=None,
                      compound="continously")
    nB = BinomialNode("B",
                      stockvalue=22,
                      strikeprice=21,
                      r=0.04,
                      upnode=nD,
                      downnode=nE,
                      compound="continously")
    nC = BinomialNode("C",
                      stockvalue=18,
                      strikeprice=21,
                      r=0.04,
                      upnode=nE,
                      downnode=nF,
                      compound="continously")
    nA = BinomialNode("A",
                      stockvalue=20,
                      strikeprice=21,
                      r=0.04,
                      upnode=nB,
                      downnode=nC,
                      compound="continously")

    # 2. We compute our result
    nA_optionprice = nA.option_price()

    print(f"Option price, Hull (2022): {nA_optionprice}")


if __name__ == "__main__":
    main()
