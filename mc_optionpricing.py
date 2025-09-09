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


def main() -> None:
    # The asset's mean
    μ = 1.0

    # The asset's standard deviation
    σ = 0.1

    # The option's strike price
    K = 1

    # Number of time periods
    n = 10

    # Discounting factor.
    β = 0.95

    # Number of simulations
    M = 10_000  # _000

    # An Mx1-array of asset prices, randomly drawn from normal distribution
    S = np.exp(μ + σ * np.random.randn(M))

    # An Mx1-array of option returns
    return_draws = np.maximum(S - K, 0)

    # The mean (expected) option price
    P = β ** n * np.mean(return_draws)

    print(f"The Monte Carlo option price is approximately {P:3f}")


if __name__ == "__main__":
    main()
