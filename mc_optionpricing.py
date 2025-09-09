import numpy as np
# import matplotlib.pyplot as plt
# from numpy.random import randn

"""
A Monte Carlo pricing of an option.

Fixed:
    * Discount rate is risk-free, r = 0.05
    * 2 time periods, t = 0 and t = 1
    * Strike price = 38
    * Underlying asset price, S_t:
        - t=0: 40
        - t=1: 48 or 30

    * 2 possible states (?)

Doesn't matter:
    * Probabilities of movements of underlying asset.

Assumptions:
    * S_t is lognormal distributed: S_t ~ LN(μ, σ)

We simulate:
    * ?

Some of the material used:
* https://intro.quantecon.org/monte_carlo.html
"""

r = 0.05


def main() -> None:
    # Let's run on the example in:
    # https://www.youtube.com/watch?v=AukJ1gDeErw

    # The correct values should be:
    # up state: option value 10, stock value 48
    # down state: option value 0, stock value 30
    # down state: option value 0
    # stock amount: 10/18 = 0.55
    # option price: 6.35

    # 2. We compute our result
    pass

    # Some sample code copied by Frans:
    μ = 1.0
    σ = 0.1
    K = 1
    n = 10
    β = 0.95
    M = 10_000  # _000

    S = np.exp(μ + σ * np.random.randn(M))
    return_draws = np.maximum(S - K, 0)
    P = β ** n * np.mean(return_draws)

    print(f"The Monte Carlo option price is approximately {P:3f}")


if __name__ == "__main__":
    main()
