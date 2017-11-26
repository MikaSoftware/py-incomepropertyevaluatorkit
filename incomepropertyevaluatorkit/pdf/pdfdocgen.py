# -*- coding: utf-8 -*-
import os, sys
from xhtml2pdf import pisa
from incomepropertyevaluatorkit.foundation.constants import *
from incomepropertyevaluatorkit.foundation.utils import *
from incomepropertyevaluatorkit.pdf.evaluatorfileformat import *


class PDFDocGen:
    """
    Class will take financial information about a rental property and
    perform PDF generation for various reports. The following reports
    are available: evaluator.
    """

    #--------------------------------------------------------------------------#
    #                     P U B L I C  F U N C T I O N S                       #
    #--------------------------------------------------------------------------#

    def __init__(self, doc_id=PDF_EVALUATOR_DOCUMENT_ID):
        assert doc_id == "evaluator", 'Currently the only supported document is "evaluator".'
        self.set_doc_id(doc_id)

    def set_doc_id(self, doc_id):
        assert doc_id == "evaluator", 'Currently the only supported document is "evaluator".'
        self._doc_id = doc_id

    def set_doc_info(self, doc_info):
        self._doc_info = doc_info

    def generate(self, filepath):
        # Load up the document from the file.
        self.init_html_content()

        # Set our variables.
        self.update_html_content()

        # Generate our document locally.
        self.convert_html_to_pdf(self._html_content, filepath)

    #--------------------------------------------------------------------------#
    #                     P R I V A T E  F U N C T I O N S                     #
    #--------------------------------------------------------------------------#

    def init_html_content(self):
        # Get the filepath of where THIS file is located and attach to the
        # filepath the document name.
        THIS_DIR = os.path.dirname(os.path.abspath(__file__))
        filepath = THIS_DIR + "/html_document/" + self._doc_id + ".html"

        # Attempt to open the document.
        with open(filepath) as input_file_handle:
            self._html_content = input_file_handle.read()

        # sys.stderr.write( "[myScript] - Error: Could not open %s\n" % (inputFn) )
        # sys.exit(-1)

    def update_html_content(self):
        """
        Function will go through the document text and replace all the
        placeholders with the values in this dicitonary.
        """
        if self._doc_id is PDF_EVALUATOR_DOCUMENT_ID:
            self._html_content = generat_evaluator_content(self._html_content, self._doc_info)

    def convert_html_to_pdf(self, sourceHtml, outputFilename):
        """
        https://github.com/xhtml2pdf/xhtml2pdf/blob/master/doc/source/usage.rst
        """
        # Enable PDF generation logging.
        pisa.showLogging()

        # open output file for writing (truncated binary)
        resultFile = open(outputFilename, "w+b")

        # convert HTML to PDF
        pisaStatus = pisa.CreatePDF(
                sourceHtml,                # the HTML to convert
                dest=resultFile)           # file handle to recieve result

        # close output file
        resultFile.close()                 # close output file

        # return True on success and False on errors
        return pisaStatus.err
