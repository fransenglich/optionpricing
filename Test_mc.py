import math
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

        stock_price = 100
        strike_price = 10
        t = 10
        sigma = 0.1
        r = 0.04

        price = mc_optionprice(stock_price, sigma, t, r, strike_price)

        self.assertEqual(math.trunc(price), 93)


if __name__ == "__main__":
    unittest.main()
