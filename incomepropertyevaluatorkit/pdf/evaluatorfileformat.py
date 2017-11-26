# -*- coding: utf-8 -*-
import os, sys
from xhtml2pdf import pisa
from incomepropertyevaluatorkit.foundation.utils import *

"""
{
    "id": "evaluator"
    "placeholders": [
        {
            "address": "",
            "country": "",
            "province": "",
            "city": ""
        }
    ],
    "custom": [

    ]
}
"""

def generat_evaluator_content(html_content, doc_info):
    html_content = replace_all(html_content, doc_info)

    return html_content
