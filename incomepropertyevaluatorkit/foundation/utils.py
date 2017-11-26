# -*- coding: utf-8 -*-
"""
Utility functions for the 'incomepropertyevaluatorkit' python library.
"""

from decimal import Decimal
import decimal
from moneyed import Money # Third party library for "Money" datatype.


MONTHS_IN_YEAR = 12
RATE_QUANTIZE = decimal.Decimal('.0001')


def rate_decimal(f, round=decimal.ROUND_HALF_UP):
    """
    This function rounds the passed float to 2 decimal places.
    """
    if not isinstance(f, decimal.Decimal):
        f = decimal.Decimal(str(f))
    return f.quantize(RATE_QUANTIZE, rounding=round)


"""
Function will make the ``range`` function to be inclusive with the last item.

Special thanks: https://stackoverflow.com/a/4504677
"""
range_inclusive = lambda start, end: range(start, end+1)


def appreciated_value(initial_value, year, inflation_rate):
    assert isinstance(initial_value, Money), 'initial_value is not a Money class: %r' % initial_value
    assert isinstance(year, int), 'year is not a Integer class: %r' % year
    assert isinstance(inflation_rate, Decimal), 'inflation_rate is not a Decimal class: %r' % inflation_rate
    appreciated_rate = inflation_rate + decimal.Decimal(1.0)
    appreciated_rate = pow(appreciated_rate, year)
    appreciated_value = initial_value * appreciated_rate
    return appreciated_value


def return_on_investment(initial_investment_amount, total_return_amount):
    assert isinstance(initial_investment_amount, Money), 'initial_investment_amount is not a Money class: %r' % initial_investment_amount
    assert isinstance(total_return_amount, Money), 'total_return_amount is not a Money class: %r' % total_return_amount
    roi = None

    # Defensive Code: Prevent division of zero.
    if initial_investment_amount.amount == Decimal(0.00):
        return Decimal(0)

    # Formulate:
    # ROI = (Investment Gain - Investment Cost) / (Investment Cost)
    roi = total_return_amount - initial_investment_amount
    roi = roi.amount / initial_investment_amount.amount
    return rate_decimal(roi)


def replace_all(text, dic):
    """
    https://stackoverflow.com/a/6117042
    """
    for i, j in dic.items():
        text = text.replace(i, j)
    return text
