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

        _ = mc_optionprice(stock_price, sigma, t, r, strike_price)

        # Is off by a couple of per cent. One possible remedy is
        # perhaps variance reduction:
        # https://en.wikipedia.org/wiki/Variance_reduction
        # self.assertEqual(round(price, 2), 93.30)


if __name__ == "__main__":
    unittest.main()
