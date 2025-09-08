
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

# The probability
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
    __parent = None
    __up = None
    __down = None
    __S_n: float = 0.0
    __K: float = 0.0

    __iscall: bool = True

    def binomial_value(self, t: int) -> float:
        """Argument t is the tree depth, or time. First node has t=0."""

        upv = __up.binomial_value(1)
        downv = __down.binomial_value(1)


        # TODO discount
        #return p * self.__up.binomial_value() + \
               #(1 - p) * self.__down.binomial_value()

        #if self.__iscall:
            #return max(self.__S_n - self.__K, 0)
        #else:
            #return max(self.__K - self.__S_n, 0)


def main() -> None:
    # 1. We build the tree.

    # 2. We compute our result
    bv = node.binomial_value(t=0)

    print(f"The Binomial Value is {bv}.")

    pass


if __name__ == "__main__":
    main()
