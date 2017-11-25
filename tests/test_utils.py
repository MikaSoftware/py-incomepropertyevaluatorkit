# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
from datetime import datetime
from decimal import Decimal
from moneyed import Money # Third party library for "Money" datatype.
from mortgagekit.calculator import MORTGAGEKIT_MONTH, MORTGAGEKIT_SEMI_ANNUAL
from incomepropertyevaluatorkit.foundation.constants import *
from incomepropertyevaluatorkit.foundation.utils import *
from incomepropertyevaluatorkit.calculator.analyzer import *


class TestUtils(unittest.TestCase):

    def test_rate_decimal(self):
        # CASE 1
        actual = rate_decimal(3)
        self.assertEqual(actual, Decimal(3))

        # CASE 2
        actual = rate_decimal(Decimal(666.00))
        self.assertAlmostEqual(actual, Decimal(666.00))

    def test_appreciated_value(self):
        initial_value = Money(amount=666.00, currency="USD")
        inflation_rate = Decimal(0.25)
        year = 5
        expect = Money(amount=2032.47, currency="USD")
        actual = appreciated_value(initial_value, year, inflation_rate)
        self.assertAlmostEqual(actual.amount, expect.amount, 2)

    def test_return_on_investment(self):
        # CASE 1
        initial_investment_amount = Money(amount=666.00, currency="USD")
        total_return_amount = Money(amount=9990.00, currency="USD")
        actual = return_on_investment(initial_investment_amount, total_return_amount)
        expect = Decimal(14.0000)
        self.assertAlmostEqual(actual, expect, 2)

        # CASE 2
        initial_investment_amount = Money(amount=0.00, currency="USD")
        total_return_amount = Money(amount=0.00, currency="USD")
        actual = return_on_investment(initial_investment_amount, total_return_amount)
        expect = Decimal(0.0000)
        self.assertAlmostEqual(actual, expect, 2)

if __name__ == '__main__':
    unittest.main()
