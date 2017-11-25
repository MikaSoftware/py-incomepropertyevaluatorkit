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


class TestFinancialAnalyzer(unittest.TestCase):

    def test_all_rental_income_functions(self):
        RENTAL_INCOME_SAMPLE_PK = 1
        analyzer = FinancialAnalyzer()  # Initialize object we will be testing.

        # Test and verify "add_rental_income" functions.
        analyzer.add_rental_income(
            pk = RENTAL_INCOME_SAMPLE_PK,
            annual_amount_per_unit = Money(amount=12300, currency='USD'),
            frequency = Decimal(1),
            monthly_amount_per_unit = Money(amount=1025, currency='USD'),
            type_id = 1,
            name_text = "Duplex Units",
            number_of_units = Decimal(2)
        )
        self.assertIsNotNone(analyzer._rental_income_dict[RENTAL_INCOME_SAMPLE_PK])

        # Test and verify "get_total_rental_income_amount" function.
        total_rental_income_amount = analyzer.get_total_rental_income_amount()
        actual = total_rental_income_amount['monthly']
        expected = Money(amount=2050, currency='USD')
        self.assertEqual(actual.amount, expected.amount)
        actual = total_rental_income_amount['annual']
        expected = Money(amount=24600, currency='USD')
        self.assertEqual(actual.amount, expected.amount)

        # Test and verify "get_rental_income" function.
        rental_income = analyzer.get_rental_income(RENTAL_INCOME_SAMPLE_PK)
        self.assertIsNotNone(rental_income)
        self.assertEqual(rental_income['pk'], RENTAL_INCOME_SAMPLE_PK)

        # Test and verify "get_rental_income" function works with missing key.
        rental_income = analyzer.get_rental_income(666)
        self.assertIsNone(rental_income)

        # Test and verify "remove_rental_income" functions.
        analyzer.remove_rental_income(RENTAL_INCOME_SAMPLE_PK)  # (1 of 2 - Existing item.)
        analyzer.remove_rental_income(RENTAL_INCOME_SAMPLE_PK)  # (2 of 2 - Non existent item.)

    def test_all_facility_income_functions(self):
        FACILITY_INCOME_SAMPLE_PK = 1
        analyzer = FinancialAnalyzer()  # Initialize object we will be testing.

        # Test and verify "add_facility_income" functions.
        analyzer.add_facility_income(
            pk = FACILITY_INCOME_SAMPLE_PK,
            annual_amount = Money(amount=1200, currency='USD'),
            frequency = Decimal(1),
            monthly_amount = Money(amount=120, currency='USD'),
            type_id = Decimal(1),
            name_text = "Coin Operated Laundery"
        )

        self.assertIsNotNone(analyzer._facility_income_dict[FACILITY_INCOME_SAMPLE_PK])
        actual = analyzer._facility_income_dict[FACILITY_INCOME_SAMPLE_PK]['annual_amount']
        expected =  Money(amount=120, currency='USD')
        self.assertTrue(actual.amount, expected.amount)

        self.assertTrue(analyzer._facility_income_dict[FACILITY_INCOME_SAMPLE_PK]['name_text'], "Coin Operated Laundery")

        # Test and verify "get_total_facility_income_amount" function.
        total_facility_income_amount = analyzer.get_total_facility_income_amount()
        actual = total_facility_income_amount['monthly']
        expected =  Money(amount=120, currency='USD')
        self.assertEqual(actual.amount, expected.amount)

        actual = total_facility_income_amount['annual']
        expected =  Money(amount=1200, currency='USD')
        self.assertEqual(actual.amount, expected.amount)

        # Test and verify "get_facility_income" function.
        facility_income = analyzer.get_facility_income(FACILITY_INCOME_SAMPLE_PK)
        self.assertIsNotNone(facility_income)
        self.assertEqual(facility_income['pk'], FACILITY_INCOME_SAMPLE_PK)

        # Test and verify "get_facility_income" function works with missing key.
        rental_income = analyzer.get_facility_income(666)
        self.assertIsNone(rental_income)

        # Test and verify "get_facility_income" functions.
        analyzer.remove_facility_income(FACILITY_INCOME_SAMPLE_PK)  # (1 of 2 - Existing item.)
        analyzer.remove_facility_income(FACILITY_INCOME_SAMPLE_PK)  # (2 of 2 - Non existent item.)

    def test_all_expense_functions(self):
        EXPENSE_SAMPLE_PK = 1
        analyzer = FinancialAnalyzer()  # Initialize object we will be testing.

        # Test and verify "add_expense" functions.
        analyzer.add_expense(
            pk = EXPENSE_SAMPLE_PK,
            annual_amount = Money(amount=1200, currency='USD'),
            frequency = Decimal(1),
            monthly_amount = Money(amount=120, currency='USD'),
            type_id = Decimal(1),
            name_text = "Utility Bill"
        )
        self.assertIsNotNone(analyzer._expense_dict[EXPENSE_SAMPLE_PK])
        actual = analyzer._expense_dict[EXPENSE_SAMPLE_PK]['annual_amount']
        expected = Money(amount=120, currency='USD')
        self.assertTrue(actual.amount, expected.amount)

        self.assertTrue(analyzer._expense_dict[EXPENSE_SAMPLE_PK]['name_text'], "Coin Operated Laundery")

        # Test and verify "get_total_expense_amount" function.
        total_expense_amount = analyzer.get_total_expense_amount()
        actual = total_expense_amount['monthly']
        expected = Money(amount=120, currency='USD')
        self.assertEqual(actual.amount, expected.amount)
        actual = total_expense_amount['annual']
        expected = Money(amount=1200, currency='USD')
        self.assertEqual(actual.amount, expected.amount)

        # Test and verify "get_expense" function.
        expense = analyzer.get_expense(EXPENSE_SAMPLE_PK)
        self.assertIsNotNone(expense)
        self.assertEqual(expense['pk'], EXPENSE_SAMPLE_PK)

        # Test and verify "get_expense" function works with missing key.
        rental_income = analyzer.get_expense(666)
        self.assertIsNone(rental_income)

        # Test and verify "get_expense" functions.
        analyzer.remove_expense(EXPENSE_SAMPLE_PK)  # (1 of 2 - Existing item.)
        analyzer.remove_expense(EXPENSE_SAMPLE_PK)  # (2 of 2 - Non existent item.)

    def test_all_commercial_income_functions(self):
        COMMERCIAL_INCOME_SAMPLE_PK = 1
        analyzer = FinancialAnalyzer()  # Initialize object we will be testing.

        # Test and verify "add_commercial_income" functions.
        analyzer.add_commercial_income(
            pk = COMMERCIAL_INCOME_SAMPLE_PK,
            annual_amount = Money(amount=1200, currency='USD'),
            frequency = Decimal(1),
            monthly_amount = Money(amount=120, currency='USD'),
            type_id = Decimal(1),
            name_text = "Office Retail Lease"
        )
        self.assertIsNotNone(analyzer._commercial_income_dict[COMMERCIAL_INCOME_SAMPLE_PK])
        actual = analyzer._commercial_income_dict[COMMERCIAL_INCOME_SAMPLE_PK]['annual_amount']
        expected = Money(amount=120, currency='USD')
        self.assertTrue(actual.amount, expected.amount)
        self.assertTrue(analyzer._commercial_income_dict[COMMERCIAL_INCOME_SAMPLE_PK]['name_text'], "Coin Operated Laundery")

        # Test and verify "get_total_commercial_income_amount" function.
        total_commercial_income_amount = analyzer.get_total_commercial_income_amount()
        actual = total_commercial_income_amount['monthly']
        expected = Money(amount=120, currency='USD')
        self.assertEqual(actual.amount, 120)
        actual = total_commercial_income_amount['annual']
        expected = Money(amount=1200, currency='USD')
        self.assertEqual(actual.amount, expected.amount)

        # Test and verify "get_commercial_income" function.
        commercial_income = analyzer.get_commercial_income(COMMERCIAL_INCOME_SAMPLE_PK)
        self.assertIsNotNone(commercial_income)
        self.assertEqual(commercial_income['pk'], COMMERCIAL_INCOME_SAMPLE_PK)

        # Test and verify "get_commercial_income" function works with missing key.
        rental_income = analyzer.get_commercial_income(666)
        self.assertIsNone(rental_income)

        # Test and verify "get_commercial_income" functions.
        analyzer.remove_commercial_income(COMMERCIAL_INCOME_SAMPLE_PK)  # (1 of 2 - Existing item.)
        analyzer.remove_commercial_income(COMMERCIAL_INCOME_SAMPLE_PK)  # (2 of 2 - Non existent item.)

    def test_gross_income(self):
        analyzer = FinancialAnalyzer()  # Initialize object we will be testing.

        # Add three varied sample data,
        analyzer.add_commercial_income(
            pk = 1,
            annual_amount = Money(amount=1200, currency='USD'),
            frequency = Decimal(1),
            monthly_amount = Money(amount=100, currency='USD'),
            type_id = 1,
            name_text = "Office Retail Lease"
        )
        analyzer.add_rental_income(
            pk = 1,
            annual_amount_per_unit = Money(amount=12300, currency='USD'),
            frequency = Decimal(1),
            monthly_amount_per_unit = Money(amount=1025, currency='USD'),
            type_id = 1,
            name_text = "Duplex Units",
            number_of_units = Decimal(2)
        )
        analyzer.add_facility_income(
            pk = 1,
            annual_amount = Money(amount=1200, currency='USD'),
            frequency = Decimal(1),
            monthly_amount = Money(amount=100, currency='USD'),
            type_id = 1,
            name_text = "Coin Operated Laundery"
        )

        gross_income_info = analyzer.get_total_gross_income_amount()
        self.assertIsNotNone(gross_income_info)
        actual = gross_income_info['monthly']
        expected = Money(amount=2250, currency='USD')
        self.assertEqual(actual, expected)
        actual = gross_income_info['annual']
        expected = Money(amount=27000, currency='USD')
        self.assertEqual(actual, expected)

    def test_all_purchase_fee_functions(self):
        PURCHASE_FEE_SAMPLE_PK = 1
        analyzer = FinancialAnalyzer()  # Initialize object we will be testing.

        # Test and verify "add_purchase_fee" functions.
        analyzer.add_purchase_fee(
            pk = PURCHASE_FEE_SAMPLE_PK,
            name_text = "CMHC Premium",
            amount = Money(amount=1200, currency='USD')
        )
        self.assertIsNotNone(analyzer._fee_dict[PURCHASE_FEE_SAMPLE_PK])
        expected =  Money(amount=1200, currency='USD')
        actual = analyzer._fee_dict[PURCHASE_FEE_SAMPLE_PK]['amount']
        self.assertTrue(actual.amount, expected.amount)
        self.assertTrue(analyzer._fee_dict[PURCHASE_FEE_SAMPLE_PK]['name_text'], "CMHC Premium")

        # Test and verify "get_total_purchase_fee_amount" function.
        total_purchase_fee_amount = analyzer.get_total_purchase_fee_amount()
        expected = Money(amount=1200, currency='USD')
        self.assertEqual(total_purchase_fee_amount.amount, expected.amount)

        # Test and verify "get_purchase_fee" function.
        purchase_fee = analyzer.get_purchase_fee(PURCHASE_FEE_SAMPLE_PK)
        self.assertIsNotNone(purchase_fee)
        self.assertEqual(purchase_fee['pk'], PURCHASE_FEE_SAMPLE_PK)

        # Test and verify "get_purchase_fee" function works with missing key.
        rental_income = analyzer.get_purchase_fee(666)
        self.assertIsNone(rental_income)

        # Test and verify "get_purchase_fee" functions.
        analyzer.remove_purchase_fee(PURCHASE_FEE_SAMPLE_PK)  # (1 of 2 - Existing item.)
        analyzer.remove_purchase_fee(PURCHASE_FEE_SAMPLE_PK)  # (2 of 2 - Non existent item.)

    def test_get_net_income_without_mortgage(self):
        analyzer = FinancialAnalyzer()  # Initialize object we will be testing.

        # Add income
        analyzer.add_rental_income(
            pk = 1,
            annual_amount_per_unit = Money(amount=1200, currency='USD'),
            frequency = Decimal(1),
            monthly_amount_per_unit = Money(amount=100, currency='USD'),
            type_id = 1,
            name_text = "Granny suite",
            number_of_units = Decimal(1)
        )

        # Add expense.
        analyzer.add_expense(
            pk = 1,
            annual_amount = Money(amount=120, currency='USD'),
            frequency = Decimal(1),
            monthly_amount = Money(amount=10, currency='USD'),
            type_id = 1,
            name_text = "Netflix"
        )

        net_income_info = analyzer.get_net_income_without_mortgage()
        self.assertIsNotNone(net_income_info)
        expected = Money(amount=90, currency='USD')
        actual = net_income_info['monthly']
        self.assertEqual(actual.amount, expected.amount)
        expected = Money(amount=1080, currency='USD')
        actual = net_income_info['annual']
        self.assertEqual(actual.amount, expected.amount)

    def test_get_net_income_with_mortgage(self):
        analyzer = FinancialAnalyzer()  # Initialize object we will be testing.

        # Add Mortgage
        analyzer.set_mortgage(
            total_amount = Money(amount=250000, currency='USD'),
            down_payment = Money(amount=50000, currency='USD'),
            amortization_year = 25,
            annual_interest_rate = Decimal(0.04),
            payment_frequency = Decimal(MORTGAGEKIT_MONTH),
            compounding_period = Decimal(MORTGAGEKIT_SEMI_ANNUAL),
            first_payment_date = '2008-01-01'
        )

        # Add income
        analyzer.add_rental_income(
            pk = 1,
            annual_amount_per_unit = Money(amount=24000, currency='USD'),
            frequency = Decimal(1),
            monthly_amount_per_unit = Money(amount=2000, currency='USD'),
            type_id = 1,
            name_text = "Granny suite",
            number_of_units = Decimal(1)
        )
        cash_flow_info = analyzer.get_net_income_with_mortgage()
        self.assertIsNotNone(cash_flow_info)
        actual = cash_flow_info['monthly']
        expected = Money(amount=947.96, currency='USD')
        self.assertAlmostEqual(actual.amount, expected.amount, 2)
        actual = cash_flow_info['annual']
        expected = Money(amount=11375.52, currency='USD')
        self.assertAlmostEqual(actual.amount, expected.amount, 2)

    def test_all_captial_improvements_functions(self):
        CAPITAL_IMPROVEMENTS_SAMPLE_PK = 1
        analyzer = FinancialAnalyzer()  # Initialize object we will be testing.

        # Test and verify "add_capital_improvement" functions.
        analyzer.add_capital_improvement(
            pk = CAPITAL_IMPROVEMENTS_SAMPLE_PK,
            name_text = "Repaired Roof",
            amount = Money(amount=1200, currency='USD')
        )
        self.assertIsNotNone(analyzer._capital_improvements_dict[CAPITAL_IMPROVEMENTS_SAMPLE_PK])
        actual = analyzer._capital_improvements_dict[CAPITAL_IMPROVEMENTS_SAMPLE_PK]['amount']
        expected = Money(amount=1200, currency='USD')
        self.assertTrue(actual.amount, expected.amount)
        self.assertTrue(analyzer._capital_improvements_dict[CAPITAL_IMPROVEMENTS_SAMPLE_PK]['name_text'], "CMHC Premium")

        # Test and verify "get_total_capital_improvements_amount" function.
        total_capital_improvement = analyzer.get_total_capital_improvements_amount()
        expected = Money(amount=1200, currency='USD')
        self.assertEqual(total_capital_improvement.amount, expected.amount)

        # Test and verify "get_capital_improvement" function.
        capital_improvement = analyzer.get_capital_improvement(CAPITAL_IMPROVEMENTS_SAMPLE_PK)
        self.assertIsNotNone(capital_improvement)
        self.assertEqual(capital_improvement['pk'], CAPITAL_IMPROVEMENTS_SAMPLE_PK)

        # Test and verify "get_capital_improvement" function works with missing key.
        rental_income = analyzer.get_capital_improvement(666)
        self.assertIsNone(rental_income)

        # Test and verify "get_capital_improvement" functions.
        analyzer.remove_capital_improvement(CAPITAL_IMPROVEMENTS_SAMPLE_PK)  # (1 of 2 - Existing item.)
        analyzer.remove_capital_improvement(CAPITAL_IMPROVEMENTS_SAMPLE_PK)  # (2 of 2 - Non existent item.)

    def test_get_total_initial_investment_amount(self):
        analyzer = FinancialAnalyzer()  # Initialize object we will be testing.

        # Test and verify "add_capital_improvement" functions.
        analyzer.add_capital_improvement(
            pk = 1,
            name_text = "Repaired Roof",
            amount = Money(amount=1200, currency='USD')
        )
        analyzer.add_purchase_fee(
            pk = 1,
            name_text = "CMHC Premium",
            amount = Money(amount=1200, currency='USD')
        )

        # Test and verify "get_total_capital_improvements_amount" function.
        total_initial_investment = analyzer.get_total_initial_investment_amount()
        self.assertIsNotNone(total_initial_investment)
        expected = Money(amount=2400, currency='USD')
        self.assertEqual(total_initial_investment.amount, expected.amount)

    def test_get_cap_rate_with_mortgage_expense_included(self):
        analyzer = FinancialAnalyzer()  # Initialize object we will be testing.

        # Purchase Price & Inflation, & fees, etc.
        analyzer.set_purchase_price(Money(amount=250000, currency='USD'))
        analyzer.set_inflation_rate(Decimal(0.025))  # 2.5%

        # Mortgage
        analyzer.set_mortgage(
            total_amount = Money(amount=250000, currency='USD'),
            down_payment = Money(amount=50000, currency='USD'),
            amortization_year = 25,
            annual_interest_rate = Decimal(0.04),
            payment_frequency = MORTGAGEKIT_MONTH,
            compounding_period = MORTGAGEKIT_SEMI_ANNUAL,
            first_payment_date = '2008-01-01'
        )

        # Perform computation.
        cap_rate = analyzer.get_cap_rate_with_mortgage_expense_included()
        self.assertIsNotNone(cap_rate)

        # Extra test case where nothing was entered.
        analyzer._purchase_price = Money(amount=0.00, currency='USD')
        cap_rate = analyzer.get_cap_rate_with_mortgage_expense_included()
        self.assertIsNotNone(cap_rate)

    def test_get_cap_rate_with_mortgage_expense_excluded(self):
        analyzer = FinancialAnalyzer()  # Initialize object we will be testing.

        # Purchase Price & Inflation, & fees
        analyzer.set_purchase_price(Money(amount=250000, currency='USD'))

        # Mortgage
        analyzer.set_mortgage(
            total_amount = Money(amount=250000, currency='USD'),
            down_payment = Money(amount=50000, currency='USD'),
            amortization_year = 25,
            annual_interest_rate = Decimal(0.04),
            payment_frequency = MORTGAGEKIT_MONTH,
            compounding_period = MORTGAGEKIT_SEMI_ANNUAL,
            first_payment_date = '2008-01-01'
        )

        # Perform computation.
        cap_rate = analyzer.get_cap_rate_with_mortgage_expense_excluded()
        self.assertIsNotNone(cap_rate)

        # Extra test case where nothing was entered.
        analyzer._purchase_price = Money(amount=0.00, currency='USD')
        cap_rate = analyzer.get_cap_rate_with_mortgage_expense_excluded()
        self.assertIsNotNone(cap_rate)

    def test_run_analysis_1(self):
        """
        """
        analyzer = FinancialAnalyzer()  # Initialize object we will be testing.

        # Purchase Price & Inflation, & fees
        analyzer.set_purchase_price(Money(amount=250000, currency='USD'))
        analyzer.set_inflation_rate(Decimal(0.025))  # 2.5%
        analyzer.set_selling_fee_rate(Decimal(0.06)) # 6.0%
        analyzer.set_buying_fee_rate(Decimal(0.006)) # 0.06 %

        # Mortgage
        analyzer.set_mortgage(
            total_amount = Money(amount=250000, currency='USD'),
            down_payment = Money(amount=50000, currency='USD'),
            amortization_year = 25,
            annual_interest_rate = Decimal(0.04),
            payment_frequency = MORTGAGEKIT_MONTH,
            compounding_period = MORTGAGEKIT_SEMI_ANNUAL,
            first_payment_date = '2008-01-01'
        )

        # DEVELOPER NOTES:
        # - The above numbers will result with:
        #     - Mortgage Amount: $200,000.00
        #     - Property Value: $250,000.00
        #     - Total Monthly Payment: $1,052.04
        #     - Loan To Value Ratio: 80.00%
        # - Verified by third party tool:
        #     - http://mortgagecalculatorcanada.com/en/calculators/mortgage-payment-calculator/

        # Rental Income
        analyzer.add_rental_income(
            pk = 1,
            annual_amount_per_unit = Money(amount=12300, currency='USD'),
            frequency = Decimal(1),
            monthly_amount_per_unit = Money(amount=1025, currency='USD'),
            type_id = 1,
            name_text = "Duplex Units",
            number_of_units = Decimal(2)
        )

        # Purchase fees.
        analyzer.add_purchase_fee(1, "CMHC Premium", Money(amount=4375, currency='USD'))
        analyzer.add_purchase_fee(2, "Down Payment", Money(amount=50000, currency='USD'))
        analyzer.add_purchase_fee(3, "Land Transfer Tax", Money(amount=2225, currency='USD'))
        analyzer.add_purchase_fee(4, "Legal Fees", Money(amount=1500, currency='USD'))

        # Expenses.
        analyzer.add_expense(
            1,
            Money(amount=3222, currency='USD'),
            Decimal(1),
            Money(amount=268.50, currency='USD'),
            1,
            "Property Tax",)
        analyzer.add_expense(
            2,
            Money(amount=2000.04, currency='USD'),
            Decimal(1),
            Money(amount=166.67, currency='USD'),
            1,
            "Maintenance")
        analyzer.add_expense(
            3,
            Money(amount=2118.24, currency='USD'),
            Decimal(1),
            Money(amount=176.52, currency='USD'),
            1,
            "Maintenance")

        # Perform computations.
        results = analyzer.perform_analysis()

        #--------------------#
        # Verify 'analysis'. #
        #--------------------#
        # Analysis
        self.assertIsNotNone(results['analysis'])

        # Verify 'rental income'.
        actual = results['analysis']['monthly_rental_income']
        expected = Money(amount=2050, currency='USD')
        self.assertEqual(actual.amount, expected.amount)

        # Verify 'expense'.
        actual = results['analysis']['monthly_expense']
        expected = Money(amount=611.69, currency='USD')
        self.assertEqual(actual.amount, expected.amount)
        actual = results['analysis']['annual_expense']
        expected = Money(amount=7340.28, currency='USD')
        self.assertEqual(actual.amount, expected.amount)

        # Verify 'purchase fees'.
        actual = results['analysis']['purchase_fees_amount']
        expected = Money(amount=58100, currency='USD')
        self.assertEqual(actual.amount, expected.amount)

        # Verify 'capital_improvement'.
        actual = results['analysis']['capital_improvements_amount']
        expected =  Money(amount=0, currency='USD')
        self.assertEqual(actual.amount, expected.amount)

        # Verify 'initial_investment_amount'.
        actual = results['analysis']['initial_investment_amount']
        expected =  Money(amount=58100, currency='USD')
        self.assertEqual(actual.amount, expected.amount)

        # Verify 'mortgage'
        actual = results['mortgage']['monthly_mortgage_payment']
        expected = Money(amount=1052.04, currency='USD')
        self.assertAlmostEqual(actual.amount, expected.amount, 2)

        actual = results['mortgage']['annual_mortgage_payment']
        expected =  Money(amount=12624.48, currency='USD')
        self.assertAlmostEqual(actual.amount, expected.amount, 2)

        # Verify 'cap_rate'.
        self.assertAlmostEqual(results['analysis']['cap_rate_with_mortgage'], Decimal(1.85), 2)
        self.assertAlmostEqual(results['analysis']['cap_rate_without_mortgage'], Decimal(6.90), 2)

        # DEVELOPER NOTE:
        # - https://itunes.apple.com/US/app/id783714275?mt=8
        # - Above "cap_rate" was verified with "Income Property Evaluator".

        # Annual projections.
        self.assertIsNotNone(results['annual_projections'])
        #TODO: WRITE MORE CODE TO VERIFY THE ANNUAL PROJECTS.

if __name__ == '__main__':
    unittest.main()
