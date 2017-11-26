# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
import os
import json
from datetime import datetime
from decimal import Decimal
from moneyed import Money # Third party library for "Money" datatype.
from mortgagekit.calculator import MORTGAGEKIT_MONTH, MORTGAGEKIT_SEMI_ANNUAL
from incomepropertyevaluatorkit.foundation.constants import *
from incomepropertyevaluatorkit.foundation.utils import *
from incomepropertyevaluatorkit.calculator.analyzer import *
from incomepropertyevaluatorkit.pdf.pdfdocgen import *


THIS_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_SAMPLE_FILEPATH = THIS_TEST_DIR+"/"+"evaluator_sample.json"
TEST_OUTPUT_FILEPATH = THIS_TEST_DIR+"/"+"file.pdf"


class TestPDFDocGen(unittest.TestCase):

    def test_generate_evaluator_doc(self):
        # Open up our JSON file with sample data to test with our class.
        with open(TEST_SAMPLE_FILEPATH) as input_file_handle:
            doc_content = json.load(input_file_handle)

        # Test that the code works.
        pdf_docgen = PDFDocGen(PDF_EVALUATOR_DOCUMENT_ID)
        pdf_docgen.set_doc_content(doc_content)
        pdf_docgen.generate(TEST_OUTPUT_FILEPATH)

        # Verify that a file does get generated.
        self.assertTrue(os.path.isfile(TEST_OUTPUT_FILEPATH))

        # DEVELOPERS NOTE:
        # The above code only confirms that a PDF was generated and thus it
        # is the responsibility of the python developer to open the PDF file
        # and validate the GUI is up to spec. Therefore the quality of the GUI
        # will be done manually be the python developer.

        # Delete the file once tested.
        os.remove(TEST_OUTPUT_FILEPATH)

if __name__ == '__main__':
    unittest.main()
