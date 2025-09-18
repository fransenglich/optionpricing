import unittest

from BinomialNode import BinomialNode


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

    # We test a call option in one step. See Hull (2022), figure 13.1.
    def test_Hull31(self):
        hull_nu = BinomialNode("U",
                               stockvalue=22,
                               strikeprice=21,
                               r=0.04,
                               upnode=None,
                               downnode=None,
                               compound="continously",
                               T=0.25)
        hull_nd = BinomialNode("D",
                               stockvalue=18,
                               strikeprice=21,
                               r=0.04,
                               upnode=None,
                               downnode=None,
                               compound="continously",
                               T=0.25)
        hull_np = BinomialNode("P",
                               stockvalue=20,
                               strikeprice=21,
                               r=0.04,
                               upnode=hull_nu,
                               downnode=hull_nd,
                               compound="continously",
                               T=0.25)

        hull_price = hull_np.option_price()

        self.assertEqual(round(hull_price, 3), 0.545)

    # We test the example in Hull (2022) p. 295, figure 13.4.
    def test_Hull134(self):
        nD = BinomialNode("D",
                          stockvalue=24.2,
                          strikeprice=21,
                          r=0.04,
                          upnode=None,
                          downnode=None,
                          compound="continously",
                          T=0.25)
        nE = BinomialNode("E",
                          stockvalue=19.8,
                          strikeprice=21,
                          r=0.04,
                          upnode=None,
                          downnode=None,
                          compound="continously",
                          T=0.25)
        nF = BinomialNode("F",
                          stockvalue=16.2,
                          strikeprice=21,
                          r=0.04,
                          upnode=None,
                          downnode=None,
                          compound="continously",
                          T=0.25)
        nB = BinomialNode("B",
                          stockvalue=22,
                          strikeprice=21,
                          r=0.04,
                          upnode=nD,
                          downnode=nE,
                          compound="continously",
                          T=0.25)
        nC = BinomialNode("C",
                          stockvalue=18,
                          strikeprice=21,
                          r=0.04,
                          upnode=nE,
                          downnode=nF,
                          compound="continously",
                          T=0.25)
        nA = BinomialNode("A",
                          stockvalue=20,
                          strikeprice=21,
                          r=0.04,
                          upnode=nB,
                          downnode=nC,
                          compound="continously",
                          T=0.25)

        # 2. We compute our result
        nA_optionprice = nA.option_price()

        self.assertEqual(round(nA_optionprice, 4), 0.9497)


if __name__ == "__main__":
    unittest.main()
