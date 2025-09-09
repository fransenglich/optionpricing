
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

    It has been tested for two time periods, t=0 and t=1.

    Some of the material used:
    * Options, Futures and Other Derivatives. John C. Hull (2022)
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
        """A vanilla init function."""

        self.stockvalue = stockvalue
        self.__strikeprice = strikeprice
        self.__upnode = upnode
        self.__downnode = downnode

    def option_price(self) -> float:
        """Returns the option price for the state this node represent in an
        binomial tree."""

        if not self.__upnode:
            assert not self.__downnode, "Both children should be None."
            # We're a leaf.

            # (We for now assume we're a call option.)
            # We know our value because the stock value and strike price is
            # known.
            option_price = max(self.stockvalue - self.__strikeprice, 0)
            print(f"Leaf, returning option value {option_price}.")
            return option_price

        call_up = self.__upnode.option_price()
        call_down = self.__downnode.option_price()

        # The amount of shares for our riskless portfolio.
        amount = (call_up - call_down) / (self.__upnode.stockvalue -
                                          self.__downnode.stockvalue)
        print(f"The stock amount is {amount}.")

        # The equation for the portfolio value is:
        #   V = amount * stockvalue - option
        # We can choose both call_up and call_down

        V = amount * self.__upnode.stockvalue - call_up
        print(f"Portfolio value is {V}.")

        # Our discount rate. Risk-free, corresponding to the life of the
        # option.
        r = 0.05  # Matches the example in the Youtube video.
        assert r > 0 and r < 1

        # We discount one time period discretely, to present value.
        PV = V / (1 + r)

        # The amount of the stock value.
        owned_stockvalue = amount * self.stockvalue

        call_value = owned_stockvalue - PV
        print(f"The option value is {call_value}.")

        return call_value


def main() -> None:
    # Let's run on the example in:
    # https://www.youtube.com/watch?v=AukJ1gDeErw

    # 1. We build the tree and specify our data.
    nu = BinomialNode(stockvalue=48, strikeprice=38, upnode=None,
                      downnode=None)
    nd = BinomialNode(stockvalue=30, strikeprice=38, upnode=None,
                      downnode=None)
    np = BinomialNode(stockvalue=40, strikeprice=38, upnode=nu,
                      downnode=nd)

    nu.parentnode = np
    nd.parentnode = np

    # The correct values should be:
    # up state: option value 10, stock value 48
    # down state: option value 0, stock value 30
    # stock amount: 10/18 = 0.55
    # option price: 6.35

    # 2. We compute our result
    _ = np.option_price()
    # The computed values matches the example on Youtube.


if __name__ == "__main__":
    main()
