import numpy as np


def black_scholes(volatility: float,
                  asset_price: float,
                  strike_price: float,
                  time_expiration: int,
                  risk_free: float) -> float:

    sd_s = 1  # standard deviation
    sd_v = 1  # standard deviation

    d1 = (np.lognormal() + (risk_free + sd_v ** 2 / 2) * time_expiration) \
        / \
        (sd_s * np.sqrt(time_expiration))

    d2 = d1 - sd_s * np.sqrt(time_expiration)

    rng = np.random.default_rng()
    rng.random()

    C = asset_price * rng.standard_normal(d1) - \
        strike_price * np.exp(-risk_free * time_expiration) \
        * rng.standard_normal(d2)

    return C


def main() -> None:
    pass


if __name__ == "__main__":
    main()
