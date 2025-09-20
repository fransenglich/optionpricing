import numpy as np
from scipy.stats import norm


def blackscholes(asset_price: float,
                 strike_price: float,
                 time_expiration: float,
                 risk_free: float,
                 volatility: float,
                 iscall: bool) -> float:
    """A closed-form implementation of the Black-Scholes-Merton (BSM) equation
    for option pricing.

    It is essentially a numerical implementation of the equation.

    Sources used:
    - John C. Hull (2022). Options, Futures and Other Derivatives.
    - https://www.macroption.com/black-scholes-formula/
    - https://www.omnicalculator.com/finance/black-scholes#how-to-calculate-black-scholes-model-black-scholes-formula
    """

    # Dividing the equation into the parts d1, d2, C, and P is customary for
    # BSM

    d1 = np.log(asset_price / strike_price) + \
        ((risk_free + volatility ** 2 / 2) * time_expiration) \
        / (volatility * np.sqrt(time_expiration))

    d2 = d1 - volatility * np.sqrt(time_expiration)

    # Note: We use the CDF, not a random Gaussian dist., because we're closed
    # form. See Hull (2022), page 353.

    if iscall:
        C = asset_price * norm.cdf(d1) - \
            strike_price * np.exp(-risk_free * time_expiration) \
            * norm.cdf(d2)
        return C
    else:
        # The dividend yield as percentage. We assume none.
        q = 0.0

        P = strike_price * np.exp(-risk_free * time_expiration) \
            * norm.cdf(-d2) \
            - \
            asset_price * np.exp(-q * time_expiration) * norm.cdf(-d1)
        return P
