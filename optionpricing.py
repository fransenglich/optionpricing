
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

# Our volatility
sigma = 1.5


class Node:
    """
    Some of the material used:
    * https://www.youtube.com/watch?v=AukJ1gDeErw
    * https://www.youtube.com/watch?v=eA5AtTx3rRI
    * https://www.youtube.com/watch?v=TynVUrat0nY
    * https://www.youtube.com/watch?v=PZrmOh2nZus
    """
    parent = None
    stockvalue: float = None


    __upnode = None
    __downnode = None
    __S_n: float = 0.0
    __K: float = 0.0
    __iscall: bool = True
    S_0 = 40


    def __init__(stockvalue, strikeprice, up_node, down_node):
        self.stockvalue = stockvalue
        self.__strikeprice = strikeprice
        self.__upnode = up_node
        self.__downnode = up_down


    def option_value(self) -> float:
        """"""

        if not self.__upnode:
            assert not self.__downnode, "Both children should be None."
            # We're a leaf

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


    def binomial_value(self) -> float:
        """We want to compute the option value."""

        # delta is the amount of shares we need to buy.
        delta: float = 0

        S_up =  # __upnode.binomial_value(1)
        S_down =  # __downnode.binomial_value(1)

        # Strike price of option.
        X

        # The call value is the stock's current value, S, minus strike price.
        option_value: float = None

        if not __upnode:
            assert not __downnode, "Both children should be None."
            # We're a leaf, the last node.
            option_value = 
        else:


        S - X

        V_up = delta * S_up - max(c_up, 0)
        V_down = delta * S_down - max(call_value, 0)

        # This is the requirement for a riskless portfolio: V_up == V_down

        delta * S_up == delta * S_down - max(call_value, 0) + max(c_up, 0)



        # TODO discount
        #return p * self.__upnode.binomial_value() + \
               #(1 - p) * self.__downnode.binomial_value()

        #if self.__iscall:
            #return max(self.__S_n - self.__K, 0)
        #else:
            #return max(self.__K - self.__S_n, 0)


def main() -> None:
    # 1. We build the tree and specify our data.
    nu = Node(stockvalue = 48, strikeprice = 38, None, None)
    nd = Node(stockvalue = 30, strikeprice = 38, None, None)
    np = Node(stockvalue = 40, strikeprice = 38, nu, nd)
    nu.parent = np
    nd.parent = np

    # 2. We compute our result
    bv = node.binomial_value(t=0)

    print(f"The Binomial Value is {bv}.")

    pass


if __name__ == "__main__":
    main()
