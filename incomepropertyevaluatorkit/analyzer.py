# -*- coding: utf-8 -*-
"""
Python library for performing rental and income property calculations.
See README for more details.
"""

from __future__ import print_function
import sys
import argparse
from datetime import datetime, timedelta
from decimal import Decimal
import math
import numpy as np  # Third party library to utilize "irr" function.
from moneyed import Money # Third party library for "Money" datatype.
from mortgagekit.calculator import *
from incomepropertyevaluatorkit.utils import *
from incomepropertyevaluatorkit.constants import MAX_YEAR


__author__ = "Bartlomiej Mika"
__copyright__ = "Copyright (c) 2017, Mika Software Corporation"
__credits__ = ["Bartlomiej Mika", "David Stubbs"]
__license__ = "BSD 2-Clause License"
__version__ = "1.0.0"
__maintainer__ = "Mika Software Corporation"
__email = "bart@mikasoftware.com"
__status__ = "Production"


class FinancialAnalyzer:
    """
    Class will take financial information about a rental property and
    perform various calculations on it to get investor data.
    """

    #--------------------------------------------------------------------------#
    #                     P U B L I C  F U N C T I O N S                       #
    #--------------------------------------------------------------------------#

    def __init__(self, currency='USD'):
        self._currency = currency
        self._purchase_price = Money(amount=0, currency=currency)
        self._inflation_rate = Money(amount=0, currency=currency)
        self._selling_fee_rate = Money(amount=0, currency=currency)
        self._buying_fee_rate = Money(amount=0, currency=currency)
        self._mortgage_calculator = None
        self._mortgage_payment_schedule = None
        self._rental_income_dict = {}
        self._facility_income_dict = {}
        self._expense_dict = {}
        self._commercial_income_dict = {}
        self._fee_dict = {}
        self._capital_improvements_dict = {}

    def set_purchase_price(self, purchase_price):
        assert isinstance(purchase_price, Money), 'purchase_price is not a Money class: %r' % purchase_price
        self._purchase_price = purchase_price

    def set_inflation_rate(self, inflation_rate):
        assert isinstance(inflation_rate, Decimal), 'inflation_rate is not a Decimal class: %r' % inflation_rate
        self._inflation_rate = inflation_rate

    def set_selling_fee_rate(self, selling_fee_rate):
        self._selling_fee_rate = selling_fee_rate

    def set_buying_fee_rate(self, buying_fee_rate):
        self._buying_fee_rate = buying_fee_rate
    #
    def set_mortgage(self, total_amount, down_payment, amortization_year,
                    annual_interest_rate, payment_frequency, compounding_period,
                    first_payment_date):
        assert isinstance(total_amount, Money), 'total_amount is not a Money class: %r' % total_amount
        assert isinstance(down_payment, Money), 'down_payment is not a Money class: %r' % down_payment
        assert isinstance(amortization_year, int), 'amortization_year is not a Integer class: %r' % amortization_year
        assert isinstance(annual_interest_rate, Decimal), 'annual_interest_rate is not a Decimal class: %r' % annual_interest_rate
        assert isinstance(payment_frequency, Decimal), 'payment_frequency is not a Decimal class: %r' % payment_frequency
        assert isinstance(compounding_period, Decimal), 'compounding_period is not a Decimal class: %r' % compounding_period
        self._mortgage_calculator = MortgageCalculator(
            total_amount,
            down_payment,
            amortization_year,
            annual_interest_rate,
            payment_frequency,
            compounding_period,
            first_payment_date
        )

    def add_rental_income(self, pk, annual_amount_per_unit, frequency, monthly_amount_per_unit, type_id, name_text, number_of_units):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        assert type(annual_amount_per_unit) is Money, "annual_amount_per_unit is not a Money class: %r" % annual_amount_per_unit
        assert type(monthly_amount_per_unit) is Money, "monthly_amount_per_unit is not a Money class: %r" % monthly_amount_per_unit
        assert type(frequency) is Decimal, "frequency is not a Decimal class: %r" % frequency
        assert type(number_of_units) is Decimal, "monthly_amount_per_unit is not a Decimal class: %r" % number_of_units
        assert isinstance(name_text, str), 'name_text is not a String class: %r' % name_text
        assert isinstance(number_of_units, Decimal), 'number_of_units is not a Decimal class: %r' % number_of_units
        self._rental_income_dict[pk] = {
            'pk': pk,
            'annual_amount_per_unit': annual_amount_per_unit,
            'frequency': frequency,
            'monthly_amount_per_unit': monthly_amount_per_unit,
            'type_id': type_id,
            'name_text': name_text,
            'number_of_units': number_of_units
        }

    def remove_rental_income(self, pk):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        try:
            del self._rental_income_dict[pk]
        except KeyError:
            pass

    def get_rental_income(self, pk):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        try:
            return self._rental_income_dict[pk]
        except KeyError:
            return None

    def add_facility_income(self, pk, annual_amount, frequency, monthly_amount, type_id, name_text):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        assert type(annual_amount) is Money, "annual_amount is not a Money class: %r" % annual_amount
        assert type(monthly_amount) is Money, "monthly_amount is not a Money class: %r" % monthly_amount
        assert type(frequency) is Decimal, "frequency is not a Decimal class: %r" % frequency
        assert isinstance(name_text, str), 'name_text is not a String class: %r' % name_text
        self._facility_income_dict[pk] = {
            'pk': pk,
            'annual_amount': annual_amount,
            'frequency': frequency,
            'monthly_amount': monthly_amount,
            'type_id': type_id,
            'name_text': name_text,
        }

    def remove_facility_income(self, pk):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        try:
            del self._facility_income_dict[pk]
        except KeyError:
            pass

    def get_facility_income(self, pk):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        try:
            return self._facility_income_dict[pk]
        except KeyError:
            return None

    def add_expense(self, pk, annual_amount, frequency, monthly_amount, type_id, name_text):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        assert type(annual_amount) is Money, "annual_amount is not a Money class: %r" % annual_amount
        assert type(monthly_amount) is Money, "monthly_amount is not a Money class: %r" % monthly_amount
        assert type(frequency) is Decimal, "frequency is not a Decimal class: %r" % frequency
        assert isinstance(name_text, str), 'name_text is not a String class: %r' % name_text
        self._expense_dict[pk] = {
            'pk': pk,
            'annual_amount': annual_amount,
            'frequency': frequency,
            'monthly_amount': monthly_amount,
            'type_id': type_id,
            'name_text': name_text,
        }

    def remove_expense(self, pk):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        try:
            del self._expense_dict[pk]
        except KeyError:
            pass

    def get_expense(self, pk):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        try:
            return self._expense_dict[pk]
        except KeyError:
            return None

    def add_commercial_income(self, pk, annual_amount, frequency, monthly_amount, type_id, name_text):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        assert type(annual_amount) is Money, "annual_amount is not a Money class: %r" % annual_amount
        assert type(monthly_amount) is Money, "monthly_amount is not a Money class: %r" % monthly_amount
        assert type(frequency) is Decimal, "frequency is not a Decimal class: %r" % frequency
        assert isinstance(name_text, str), 'name_text is not a String class: %r' % name_text
        self._commercial_income_dict[pk] = {
            'pk': pk,
            'annual_amount': annual_amount,
            'frequency': frequency,
            'monthly_amount':monthly_amount,
            'type_id': type_id,
            'name_text': name_text,
        }

    def remove_commercial_income(self, pk):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        try:
            del self._commercial_income_dict[pk]
        except KeyError:
            pass

    def get_commercial_income(self, pk):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        try:
            return self._commercial_income_dict[pk]
        except KeyError:
            return None

    def add_purchase_fee(self, pk, name_text, amount):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        assert isinstance(name_text, str), 'name_text is not a String class: %r' % name_text
        assert isinstance(amount, Money), "amount is not a Money class: %r" % amount
        self._fee_dict[pk] = {
            'pk': pk,
            'name_text': name_text,
            'amount': amount
        }

    def get_purchase_fee(self, pk):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        try:
            return self._fee_dict[pk]
        except KeyError:
            return None

    def remove_purchase_fee(self, pk):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        try:
            del self._fee_dict[pk]
        except KeyError:
            pass

    def add_capital_improvement(self, pk, name_text, amount):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        assert isinstance(name_text, str), 'name_text is not a String class: %r' % name_text
        assert isinstance(amount, Money), "amount is not a Money class: %r" % amount
        self._capital_improvements_dict[pk] = {
            'pk': pk,
            'name_text': name_text,
            'amount': amount
        }

    def get_capital_improvement(self, pk):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        try:
            return self._capital_improvements_dict[pk]
        except KeyError:
            return None

    def remove_capital_improvement(self, pk):
        assert isinstance(pk, int), 'pk is not a Integer class: %r' % pk
        try:
            del self._capital_improvements_dict[pk]
        except KeyError:
            pass

    def perform_analysis(self):
        #  // Steps 1-3:
        self.perform_computation_on_mortgage()

        # // Step 4: Perform a summation/subtraction on all the information to get
        # //         aggregate data.
        self.perform_computation_on_analysis()

        # // Step 5: Analyze various variables for the fincial analysis
        self.perform_computation_on_annual_projections()

        # STEP 6: Return computations summary from our analysis.
        return {
            'purchase_price': self._purchase_price,
            'inflation_rate': self._inflation_rate,
            'selling_fee_rate': self._selling_fee_rate,
            'buying_fee_rate': self._buying_fee_rate,
            'rental_incomes': self._rental_income_dict,
            'facility_incomes': self._facility_income_dict,
            'expenses': self._expense_dict,
            'commercial_incomes': self._commercial_income_dict,
            'purchase_fees': self._fee_dict,
            'capital_improvements': self._capital_improvements_dict,
            'mortgage': {
                'interest_rate_per_payment_frequency': self._mortgage_calculator.get_interest_rate_per_payment_frequency(),
                'total_number_of_payments_per_frequency': self._mortgage_calculator.get_total_number_of_payments_per_frequency(),
                'mortgage_payment_per_payment_frequency': self._mortgage_calculator.get_mortgage_payment_per_payment_frequency(),
                'monthly_mortgage_payment': self._mortgage_calculator.get_monthly_mortgage_payment(),
                'annual_mortgage_payment': self._mortgage_calculator.get_annual_mortgage_payment(),
                'percent_of_loan_financed': self._mortgage_calculator.get_percent_of_loan_financed(),
                'schedule': self._mortgage_payment_schedule
            },
            'analysis': {
                'monthly_rental_income': self._monthly_rental_income,
                'annual_rental_income': self._annual_rental_income,
                'monthly_facility_income': self._monthly_facility_income,
                'annual_facility_income': self._annual_facility_income,
                'monthly_expense': self._monthly_expense,
                'annual_expense': self._annual_expense,
                'monthly_gross_income': self._monthly_gross_income,
                'annual_gross_income': self._annual_gross_income,
                'monthly_net_income': self._monthly_net_income,
                'annual_net_income': self._annual_net_income,
                'monthly_cash_flow': self._monthly_cash_flow,
                'annual_cash_flow': self._annual_cash_flow,
                'purchase_fees_amount': self._purchase_fees_amount,
                'capital_improvements_amount': self._capital_improvements_amount,
                'initial_investment_amount': self._initial_investment_amount,
                'cap_rate_with_mortgage': self._cap_rate_with_mortgage,
                'cap_rate_without_mortgage': self._cap_rate_without_mortgage
            },
            'annual_projections': self._annual_projections
        }

    #--------------------------------------------------------------------------#
    #                     P R I V A T E  F U N C T I O N S                     #
    #--------------------------------------------------------------------------#

    def get_total_rental_income_amount(self):
        """
        Function sums "monthly_amount" and "annual_amount" in the
        "Rental Income" objects of this analyzer.
        """
        total_monthly_amount = Money(amount=0, currency=self._currency)
        total_annual_amount = Money(amount=0, currency=self._currency)
        keys = self._rental_income_dict.keys()
        for key in keys:
            # Get our object.
            rental_income = self._rental_income_dict[key]

            # Get the amounts.
            monthly_amount_per_unit = rental_income['monthly_amount_per_unit']
            annual_amount_per_unit = rental_income['annual_amount_per_unit']
            number_of_units = rental_income['number_of_units']

            # Sum
            total_monthly_amount += monthly_amount_per_unit * number_of_units
            total_annual_amount += annual_amount_per_unit * number_of_units
        return {
            'monthly': total_monthly_amount,
            'annual': total_annual_amount
        }

    def get_total_facility_income_amount(self):
        """
        Function sums "monthly_amount" and "annual_amount" in the
        "Facility Income" objects of this analyzer.
        """
        total_monthly_amount = Money(amount=0, currency=self._currency)
        total_annual_amount = Money(amount=0, currency=self._currency)
        keys = self._facility_income_dict.keys()
        for key in keys:
            # Get our object.
            facility_income = self._facility_income_dict[key]

            # Get the amounts & sum.
            total_monthly_amount += facility_income['monthly_amount']
            total_annual_amount += facility_income['annual_amount']
        return {
            'monthly': total_monthly_amount,
            'annual': total_annual_amount
        }

    def get_total_expense_amount(self):
        """
        Function sums "monthly_amount" and "annual_amount" in the
        "Expense" objects of this analyzer.
        """
        total_monthly_amount = Money(amount=0, currency=self._currency)
        total_annual_amount = Money(amount=0, currency=self._currency)
        keys = self._expense_dict.keys()
        for key in keys:
            # Get our object.
            expense = self._expense_dict[key]

            # Get the amounts & sum.
            total_monthly_amount += expense['monthly_amount']
            total_annual_amount += expense['annual_amount']
        return {
            'monthly': total_monthly_amount,
            'annual': total_annual_amount
        }

    def get_total_commercial_income_amount(self):
        """
        Function sums "monthly_amount" and "annual_amount" in the
        "commercial Income" objects of this analyzer.
        """
        total_monthly_amount = Money(amount=0, currency=self._currency)
        total_annual_amount = Money(amount=0, currency=self._currency)
        keys = self._commercial_income_dict.keys()
        for key in keys:
            # Get our object.
            commercial_income = self._commercial_income_dict[key]

            # Get the amounts & sum.
            total_monthly_amount += commercial_income['monthly_amount']
            total_annual_amount += commercial_income['annual_amount']
        return {
            'monthly': total_monthly_amount,
            'annual': total_annual_amount
        }

    def get_total_gross_income_amount(self):
        # Compute the individual totals.
        commercial_income_total = self.get_total_commercial_income_amount()
        rental_income_total = self.get_total_rental_income_amount()
        facility_income_total = self.get_total_facility_income_amount()

        # Compute the aggregate totals.
        total_monthly_amount = commercial_income_total['monthly'] + rental_income_total['monthly'] + facility_income_total['monthly']
        total_annual_amount = commercial_income_total['annual'] + rental_income_total['annual'] + facility_income_total['annual']

        # Return results.
        return {
            'monthly': total_monthly_amount,
            'annual': total_annual_amount
        }

    def get_total_purchase_fee_amount(self):
        """
        Function sums "monthly_amount" and "annual_amount" in the
        "commercial Income" objects of this analyzer.
        """
        total_amount = Money(amount=0, currency=self._currency)
        keys = self._fee_dict.keys()
        for key in keys:
            # Get our object.
            purchase_fee = self._fee_dict[key]

            # Get the amounts & sum.
            total_amount += purchase_fee['amount']
        return total_amount

    def get_net_income_without_mortgage(self):
        gross_income_info = self.get_total_gross_income_amount()
        expense_info = self.get_total_expense_amount()
        return {
            'monthly': gross_income_info['monthly'] - expense_info['monthly'],
            'annual': gross_income_info['annual'] - expense_info['annual'],
        }

    def get_net_income_with_mortgage(self):
        net_income_info = self.get_net_income_without_mortgage()

        monthly_mortgage_payment = self._mortgage_calculator.get_monthly_mortgage_payment()
        annual_mortgage_payment = self._mortgage_calculator.get_annual_mortgage_payment()

        return {
            'monthly': net_income_info['monthly'] - monthly_mortgage_payment,
            'annual': net_income_info['annual'] - annual_mortgage_payment
        }

    def get_total_capital_improvements_amount(self):
        total_amount = Money(amount=0, currency=self._currency)
        keys = self._capital_improvements_dict.keys()
        for key in keys:
            # Get our object.
            capital_improvement = self._capital_improvements_dict[key]

            # Get the amounts & sum.
            total_amount += capital_improvement['amount']
        return total_amount

    def get_total_initial_investment_amount(self):
        total_purchase_fee = self.get_total_purchase_fee_amount()
        total_capital_improvement = self.get_total_capital_improvements_amount()
        return total_purchase_fee + total_capital_improvement

    def get_cap_rate_with_mortgage_expense_included(self):
        if self._purchase_price.amount == 0:  # Defensive Code: Cannot divide by zero.
            return Money(amount=0, currency=self._currency)

        cash_flow_info = self.get_net_income_with_mortgage()
        cap_rate = cash_flow_info['annual'].amount / self._purchase_price.amount
        return Decimal(cap_rate * 100)

    def get_cap_rate_with_mortgage_expense_excluded(self):
        if self._purchase_price.amount == 0:  # Defensive Code: Cannot divide by zero.
            return Money(amount=0, currency=self._currency)

        cash_flow_info = self.get_net_income_without_mortgage()
        cap_rate = cash_flow_info['annual'].amount / self._purchase_price.amount
        cap_rate_percent = Decimal(cap_rate * 100)
        return Decimal(cap_rate_percent)

    def perform_computation_on_mortgage(self):
        self._mortgage_payment_schedule = self._mortgage_calculator.get_mortgage_payment_schedule()

    def perform_computation_on_analysis(self):
        total_amount = self.get_total_rental_income_amount()
        self._monthly_rental_income = total_amount['monthly']
        self._annual_rental_income = total_amount['annual']

        total_amount = self.get_total_facility_income_amount()
        self._monthly_facility_income = total_amount['monthly']
        self._annual_facility_income = total_amount['annual']

        total_amount = self.get_total_expense_amount()
        self._monthly_expense = total_amount['monthly']
        self._annual_expense = total_amount['annual']

        total_amount = self.get_total_gross_income_amount()
        self._monthly_gross_income = total_amount['monthly']
        self._annual_gross_income = total_amount['annual']

        total_amount = self.get_net_income_without_mortgage()
        self._monthly_net_income = total_amount['monthly']
        self._annual_net_income = total_amount['annual']

        cash_flow_info = self.get_net_income_with_mortgage()
        self._monthly_cash_flow = cash_flow_info['monthly']
        self._annual_cash_flow = cash_flow_info['annual']

        total_amount = self.get_total_purchase_fee_amount()
        self._purchase_fees_amount = total_amount

        total_amount = self.get_total_capital_improvements_amount()
        self._capital_improvements_amount = total_amount

        self._initial_investment_amount = self.get_total_initial_investment_amount()

        self._cap_rate_with_mortgage = self.get_cap_rate_with_mortgage_expense_included()
        self._cap_rate_without_mortgage = self.get_cap_rate_with_mortgage_expense_excluded()

    def debt_remaining_at_eoy(self, year, payment_schedule, mortgage_calculator):
        # Note: We need to get how many pay cycles there will be per year.
        payment_frequency_integer = mortgage_calculator.get_payment_frequency()

        # Calculate the index position of where the record we're searching for is located.
        index = (year) * payment_frequency_integer - 1;
        index = int(index)

        if index >= len(payment_schedule):
            return Money(amount=0, currency=self._currency)

        # Get our record.
        loan_balance = payment_schedule[index]['loan_balance']

        return loan_balance

    def perform_computation_on_annual_projections(self):
        """
        Note: You need to run "perform_computation_on_mortgage" before running
        this function.
        """
        # Variable which will hold all our projections on a per year basis.
        annual_projections = []

        # Calculate and extract values we'll be using throughout our computation.
        mortgage_payment_schedule = self._mortgage_payment_schedule
        mortgage_calculator = self._mortgage_calculator
        inflation_rate = self._inflation_rate
        annual_net_income_with_mortgage_info = self.get_net_income_with_mortgage()
        annual_net_income_without_mortgage_info = self.get_net_income_without_mortgage()
        sales_price = self._purchase_price
        selling_fee_rate = self._selling_fee_rate
        initial_investment_amount = self.get_total_initial_investment_amount()

        # To calculate "IRR", we will need to store the initial investment
        # (negative) and then add all the cash flows afterwords (positive).
        cash_flow_array = []
        negative_initial_investment_amount = initial_investment_amount * Decimal(-1)
        cash_flow_array.append(negative_initial_investment_amount)

        # Variable stores the previous years cash flow value.
        previous_years_cash_flow = Money(amount=0, currency=self._currency)

        for year in range_inclusive(1, MAX_YEAR):
            # Generic Calculations
            #------------------------------------------------------
            # Calculate how much debt we have remaining to pay off.
            loan_balance = self.debt_remaining_at_eoy(year, mortgage_payment_schedule, mortgage_calculator)

            # Defensive Coding: Cannot have negative 'debtRemaining' values.
            if loan_balance.amount < 0:
                loan_balance = Money(amount=0, currency=self._currency)  # Automatically set to zero if this happens.

            # Calculate how much money we have coming in at the end of the year and
            # apply appreciation to it.
            cash_flow = Money(amount=0, currency=self._currency)
            appreciated_cash_flow = Money(amount=0, currency=self._currency)
            if loan_balance.amount > 0:
                cash_flow = annual_net_income_with_mortgage_info['annual']
                appreciated_cash_flow = appreciated_value(cash_flow, year, inflation_rate)
            else:
                cash_flow = annual_net_income_without_mortgage_info['annual']
                appreciated_cash_flow = appreciated_value(cash_flow, year, inflation_rate)

            # Calculate our new sales price
            appreciated_sales_price = appreciated_value(sales_price, year, inflation_rate)

            # Calculate legal & realty domain fees
            fees = sales_price * selling_fee_rate
            appreciated_fees = appreciated_value(fees, year, inflation_rate)

            # Calculate the proceeds of sale
            proceeds_of_sale = appreciated_sales_price - appreciated_fees
            proceeds_of_sale = proceeds_of_sale - loan_balance

            # Calculate the total return
            total_return = proceeds_of_sale - appreciated_cash_flow

            # Calculate the return on investment
            roi_rate = return_on_investment(initial_investment_amount, total_return)
            roi_percent = roi_rate * Decimal(100.0)

            # Calculate Annualized Return on Investment (1 of 2)
            #---------------------------------------------------
            # STEP 1: The previous value needs to be the cash flow if it hasn't
            #         been already defined.
            if previous_years_cash_flow == None:
                previous_years_cash_flow = cash_flow

            # STEP 2: Calculate the 'net processed from sales' variable which
            #         is essential: (previous years cash flow + purchase price)
            net_processed_from_sales = previous_years_cash_flow + proceeds_of_sale

            # STEP 3: Add the final object to our cash flow array of payments.
            cash_flow_array.append(net_processed_from_sales) # IRR Code 1 of 2

            # STEP 4: Calculate our IRR.
            float_cash_flow_array = []
            for value in cash_flow_array: # Convert from Decimal to Float.
                float_cash_flow_array.append(value.amount)

            # Use the python 'numpy' library to get the 'irr' functionality
            # instead of implementing it ourselves.
            irr_rate = np.irr(float_cash_flow_array)
            irr_percent = irr_rate * 100

            # Update the MODEL with the following values
            #---------------------------------------------------
            annual_projections.append({
                'year': year,
                'debt_remaining': loan_balance,
                'sales_price': appreciated_sales_price,
                'legal_fees': appreciated_fees,
                'cash_flow': appreciated_cash_flow,
                'initial_investment': initial_investment_amount,
                'proceeds_of_sale': proceeds_of_sale,
                'total_return': total_return,
                'roi_rate': roi_rate,
                'roi_percent': roi_percent,
                'annualized_roi_rate': irr_rate,
                'annualized_roi_percent': irr_percent
            })

            # Calculate Annualized Return on Investment (2 of 2)
            #----------------------------------------------------
            # Update the cashFlow
            # However, this is not the last year! Therefore remove the total return
            # which is the last object and cashflow.
            del cash_flow_array[-1]  # IRR Code 2 of 2 - Remove last object.
            cash_flow_array.append(previous_years_cash_flow);

            previous_years_cash_flow = appreciated_cash_flow

        # Return the annual projects we have computed in this function.
        self._annual_projections = annual_projections
