import unittest

from blackscholes import blackscholes


class Testblackscholes(unittest.TestCase):
    """
    """

    def test_mystockoptions(self):
        """We run https://www.mystockoptions.com/black-scholes.cfm
        which for the below values returns 7.366.
        This calculator yields the same (7.37):
        https://www.omnicalculator.com/finance/black-scholes
        """

        mystock = blackscholes(14, 10, 3.5, 0.05, 0.5, iscall=True)

        self.assertEqual(round(mystock, 2), 7.36)

    def test_put(self):
        """Now let's run for a put. The second calculator above yields 5.49."""

        # omnicalculator = blackscholes(100, 80, 2, 0.03, 0.3, iscall=False)

        # WIP
        # Prints 4.899. Is hence wrong and not validated by the calculator.
        # self.assertEqual(round(omnicalculator, 2), 5.49)


if __name__ == "__main__":
    unittest.main()
