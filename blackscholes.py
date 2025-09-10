import numpy as np


def black_scholes(asset_price: float,
                  strike_price: float,
                  time_expiration: float,
                  risk_free: float,
                  volatility: float) -> float:
    """An implementation of the Black-Scholes-Merton (BSM) equation for option
    pricing.

    An extensive source is John C. Hull (2022). Options, Futures and Other Derivatives."""

    # Dividing the equation into the parts d1, d2, and C is customary for BSM

    d1 = np.emath.logn(strike_price, asset_price) + \
        ((risk_free + volatility ** 2 / 2) * time_expiration) \
        / (volatility * np.sqrt(time_expiration))

    d2 = d1 - volatility * np.sqrt(time_expiration)

    rng = np.random.default_rng()
    rng.random()

    C = asset_price * rng.normal(d1) - \
        strike_price * np.exp(-risk_free * time_expiration) \
        * rng.normal(d2)

    return C


def main() -> None:

    # We run https://www.mystockoptions.com/black-scholes.cfm
    # which for the below values returns 7.366.
    # This calculator yields the same (7.37):
    # https://www.omnicalculator.com/finance/black-scholes
    mso = black_scholes(14, 10, 3.5, 0.05, 0.5)

    print(f"mso: {mso}")


if __name__ == "__main__":
    main()
