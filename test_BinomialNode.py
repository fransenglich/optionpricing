import unittest

from binomialtree import BinomialNode


# Runs various found examples of option pricing
# using binomial trees.
class TestBinomialNode(unittest.TestCase):

    # We test the example in:
    # https://www.youtube.com/watch?v=AukJ1gDeErw
    def test_Youtube(self):
        nu = BinomialNode("U",
                          stockvalue=48,
                          strikeprice=38,
                          r=0.05,
                          upnode=None,
                          downnode=None)
        nd = BinomialNode("D",
                          stockvalue=30,
                          strikeprice=38,
                          r=0.05,
                          upnode=None,
                          downnode=None)
        np = BinomialNode("P",
                          stockvalue=40,
                          strikeprice=38,
                          r=0.05,
                          upnode=nu,
                          downnode=nd)

        # The correct values should be:
        # up state: option value 10, stock value 48
        # down state: option value 0, stock value 30
        # stock amount: 10/18 = 0.55
        # option price: 6.35

        ytprice = np.option_price()

        self.assertEqual(round(ytprice, 2), 6.35)


if __name__ == "__main__":
    unittest.main()
