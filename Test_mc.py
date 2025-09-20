import unittest

from mc_optionprice import mc_optionprice


class TestMC_optionprice(unittest.TestCase):
    """
    """

    def test_mystockoptions(self):
        """We run https://www.mystockoptions.com/black-scholes.cfm
        which for the below values returns 7.366.
        This calculator yields the same (7.37):
        https://www.omnicalculator.com/finance/black-scholes
        """

        # mystock = blackscholes(14, 10, 3.5, 0.05, 0.5, iscall=True)
        mu = 0.4
        sigma = 0.5
        t = 10
        r = 0.05
        asset_price = 14
        strike_price = 10

        price = mc_optionprice(asset_price, mu, sigma, t, r, strike_price)

        self.assertEqual(round(price, 2), 7.36)


if __name__ == "__main__":
    unittest.main()
