# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
import os
from datetime import datetime
from decimal import Decimal
from moneyed import Money # Third party library for "Money" datatype.
from mortgagekit.calculator import MORTGAGEKIT_MONTH, MORTGAGEKIT_SEMI_ANNUAL
from incomepropertyevaluatorkit.foundation.constants import *
from incomepropertyevaluatorkit.foundation.utils import *
from incomepropertyevaluatorkit.calculator.analyzer import *
from incomepropertyevaluatorkit.pdf.pdfdocgen import *


THIS_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILENAME = "file.pdf"
TEST_FILEPATH = THIS_TEST_DIR+"/"+TEST_FILENAME
TEST_DOC_CONTENT = {
    "id": PDF_EVALUATOR_DOCUMENT_ID,
    "text_placeholders": {
        "{{ copyrighted }}": "Copyrighted 2017 Duplexsoft",
        "{{ property_name }}": "Whiskey Cabin"
    }
}

class TestPDFDocGen(unittest.TestCase):

    def test_generate_evaluator_doc(self):
        pdf_docgen = PDFDocGen(PDF_EVALUATOR_DOCUMENT_ID)
        pdf_docgen.set_doc_content(TEST_DOC_CONTENT)
        pdf_docgen.generate(TEST_FILEPATH)

        # Confirm that a file does get generated.
        self.assertTrue(os.path.isfile(TEST_FILEPATH))

        # DEVELOPERS NOTE:
        # The above code only confirms that a PDF was generated and thus it
        # is the responsibility of the python developer to open the PDF file
        # and validate the GUI is up to spec. Therefore the quality of the GUI
        # will be done manually be the python developer.

        # Delete the file once tested.
        os.remove(TEST_FILEPATH)

if __name__ == '__main__':
    unittest.main()
