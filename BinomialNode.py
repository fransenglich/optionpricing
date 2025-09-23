import math


class BinomialNode:
    """
    A node in a binomial tree for option pricing of European options.

    It has the public variable stockvalue, and the central member function
    option_price(). The conceptuals are a bit clouded by the non-essential
    features for selection discounting method and pretty printing.

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

    def __init__(self, name: str,
                 stockvalue: float,
                 strikeprice: float,
                 r: float,
                 upnode,
                 downnode,
                 compound="discretely",
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
