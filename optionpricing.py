
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

# The probability of the asset in the binomial tree.
p = 0.7  # arbitrary
assert p > 0 and p <= 1

# Our discount rate. risk-free, corresponding to the life of the option.
r = 0.02  # arbitrary
assert r > 0 and r < 1


class Node:
    """
    A node in a binomial tree.

    Some of the material used:
    * https://www.youtube.com/watch?v=AukJ1gDeErw
    * https://www.youtube.com/watch?v=eA5AtTx3rRI
    * https://www.youtube.com/watch?v=TynVUrat0nY
    * https://www.youtube.com/watch?v=PZrmOh2nZus
    """
    parentnode = None
    stockvalue: float = None
    __upnode = None
    __downnode = None


    def __init__(self, stockvalue, strikeprice, upnode, downnode):
        self.stockvalue = stockvalue
        self.__strikeprice = strikeprice
        self.__upnode = upnode
        self.__downnode = downnode


    def option_value(self) -> float:
        """"""

        if not self.__upnode:
            assert not self.__downnode, "Both children should be None."
            # We're a leaf.

            # (We for now assume we're a call option.)
            # We know our value because the stock value and strike price is
            # known.
            return max(self.stockvalue - self.__strikeprice, 0)

        call_up = self.__upnode.option_value()
        call_down = self.__downnode.option_value()

        # The amount of shares for our riskless portfolio.
        delta = (call_up - call_down) / (self.__upnode.stockvalue - self.__downnode.stockvalue)

        # The equation for the portfolio value is:
        # V = delta * stockvalue - option

        V = delta * self.stockvalue  - call_up

        # We discount one time period.
        PV = V / (1 + r)

        # The amount of the stock value.
        owned_stockvalue = delta * self.stockvalue

        call_value = owned_stockvalue - PV

        return call_value


def main() -> None:
    # 1. We build the tree and specify our data.
    nu = Node(stockvalue=48, strikeprice=38, upnode=None, downnode=None)
    nd = Node(stockvalue=30, strikeprice=38, upnode=None, downnode=None)
    np = Node(stockvalue=40, strikeprice=38, upnode=nu, downnode=nd)
    nu.parentnode = np
    nd.parentnode = np

    # 2. We compute our result
    call_value = np.option_value()

    print(f"The option value is {call_value}.")

    pass


if __name__ == "__main__":
    main()
