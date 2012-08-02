import time
from flask import Response
from functools import wraps
from StringIO import StringIO
import pywkhtmltopdf as html_to_pdf
from pyPdf import PdfFileWriter, PdfFileReader
from pdf import Pdf

def to_pdf(duplicate=False):
    """Decorator for Flask view functions, return current html as pdf"""

    def wrap(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            function_return = f(*args, **kwargs)
            print args, kwargs;
            pdf_conv = html_to_pdf.HTMLToPDFConverter()
            html_string = StringIO(function_return.encode('utf-8'))
            if duplicate:
                encoded_pdf = duplicated_pdf(html_string)
            else:
                encoded_pdf = pdf_conv.convert(html_string)
            resp = Response(encoded_pdf, mimetype='application/pdf')
            titulo = "Recibo_%s" % int(time.time())
            resp.headers['Content-Disposition'] = 'attachment; filename="%s.pdf"' %titulo
            return resp
        return decorated
    return wrap

def duplicated_pdf(stream):
    """Creates a duplicated pdf, from html stream (A.K.A. StringIO)"""

    o_text = "<center><h3>-- Original --</h3></center>"
    c_text = "<center><h3>-- Duplicado --</h3></center>"
    pdf_conv = html_to_pdf.HTMLToPDFConverter()

    original = PdfFileReader(StringIO(pdf_conv.convert(stream, o_text, o_text)))

    stream.seek(0)
    copy = PdfFileReader(StringIO(pdf_conv.convert(stream, c_text, c_text)))

    out = PdfFileWriter()
    for n in xrange(0, original.getNumPages()):
        out.addPage(original.getPage(n))

    for n in xrange(0, copy.getNumPages()):
        out.addPage(copy.getPage(n))

    encoded_pdf = StringIO()
    out.write(encoded_pdf)

    encoded_pdf.seek(0)
    encoded_pdf = encoded_pdf.read()

    return encoded_pdf






