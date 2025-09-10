import numpy as np
from scipy.stats import norm


def black_scholes(asset_price: float,
                  strike_price: float,
                  time_expiration: float,
                  risk_free: float,
                  volatility: float,
                  iscall: bool) -> float:
    """An implementation of the Black-Scholes-Merton (BSM) equation for option
    pricing.

    Sources used:
    - An extensive source is John C. Hull (2022). Options, Futures and Other
      Derivatives.
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
    C = 0.0

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


def main() -> None:
    # We run https://www.mystockoptions.com/black-scholes.cfm
    # which for the below values returns 7.366.
    # This calculator yields the same (7.37):
    # https://www.omnicalculator.com/finance/black-scholes"""
    mystock = black_scholes(14, 10, 3.5, 0.05, 0.5, iscall=True)

    # Prints 7.36487751. Same as the two calculators.
    print(f"Call option price: {mystock}")

    # Now let's run for a put. The second calculator above yields 5.49.
    omnicalculator = black_scholes(100, 80, 2, 0.03, 0.3, iscall=False)

    # Prints 4.899. Is hence wrong and not validated by the calculator.
    print(f"Put option price: {omnicalculator}")


if __name__ == "__main__":
    main()
