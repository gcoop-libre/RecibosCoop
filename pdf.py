from flask import Response
from functools import wraps
from StringIO import StringIO
import pywkhtmltopdf as pdf


def to_pdf(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        function_return = f(*args, **kwargs)
        pdf_conv = pdf.HTMLToPDFConverter()
        html_string = StringIO(function_return.encode('utf-8'))
        encoded_pdf = pdf_conv.convert(html_string)
        return Response(encoded_pdf, mimetype='application/pdf')
    return decorated


