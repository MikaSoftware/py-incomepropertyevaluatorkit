# -*- coding: utf-8 -*-
import os, sys
from xhtml2pdf import pisa
from incomepropertyevaluatorkit.foundation.constants import *
from incomepropertyevaluatorkit.foundation.utils import *


"""
This code is responsible for taking the HTML content for the "evaluator"
document and replace all the documents placeholders with the user created
content and return a formatted and created HTML document. This outputted HTML
content will be used to generate the PDF document through the python "xhtml2pdf"
library.
"""


def set_evaluator_content(html_content, doc_content):
    """
    Function will take the "evaluator" content and replace all the
    placeholders with the user inputted content.
    """
    # Validate format.
    assert doc_content['id'] == PDF_EVALUATOR_DOCUMENT_ID

    # Handle text placeholders here.
    html_content = replace_all(html_content, doc_content['text_placeholders'])

    #TODO: IMPLEMENT DOCUMENT CREATION CODE HERE!

    return html_content
