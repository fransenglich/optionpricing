import numpy as np


def black_scholes(asset_price: float,
                  strike_price: float,
                  time_expiration: float,
                  risk_free: float,
                  volatility: float) -> float:
    """An implementation of the Black-Scholes-Merton (BSM) equation for option
    pricing."""

    sd_s = volatility
    sd_v = volatility

    # Dividing the equation into the parts d1, d2, and C is customary for BSM

    d1 = (np.emath.logn(strike_price, asset_price) +
        (risk_free + sd_v ** 2 / 2) * time_expiration) \
        / (sd_s * np.sqrt(time_expiration))

    d2 = d1 - sd_s * np.sqrt(time_expiration)

    rng = np.random.default_rng()
    rng.random()

    C = asset_price * rng.normal(d1) - \
        strike_price * np.exp(-risk_free * time_expiration) \
        * rng.normal(d2)

    return C


def main() -> None:

    # We run https://www.mystockoptions.com/black-scholes.cfm
    # which for the below values returns 7.366.
    mso = black_scholes(14, 10, 3.5, 0.05, 0.5)

    print(f"mso: {mso}")


if __name__ == "__main__":
    main()
