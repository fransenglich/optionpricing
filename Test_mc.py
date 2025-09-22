import unittest

from mc_optionprice import mc_optionprice


class TestMC_optionprice(unittest.TestCase):
    """
    Tests the Monte Carlo implementation for option pricing.
    """

    def test_basic(self):
        """We run and compare against the result from:
        https://www.omnicalculator.com/finance/black-scholes
        """

        mu = 0.4

        stock_price = 100
        strike_price = 10
        t = 10
        sigma = 0.1
        r = 0.04

        price = mc_optionprice(stock_price, mu, sigma, t, r, strike_price)
        self.assertEqual(round(price, 2), 93.30)


if __name__ == "__main__":
    unittest.main()
