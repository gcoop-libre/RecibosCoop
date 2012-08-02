from StringIO import StringIO
import pywkhtmltopdf as html_to_pdf
from pyPdf import PdfFileWriter, PdfFileReader

class Pdf(object):
    """Pdf file abstraction"""
    def __init__(self, html, filename=None):
        self.htmls = []
        self.converter = html_to_pdf.HTMLToPDFConverter()
        self.append(html)
        self.render = None

    def get_stream(self):
        """Return encoded_pdf stream"""
        first = True
        for html in self.htmls:
            print html
            if first:
                out = self.to_pdf(html)
                first = False
            else:
                out = self.concat(out, html)
        return out

    def append(self, html):
        self.htmls.append(html)

    def to_pdf(self, html):
        """Converts a html in pdf file"""
        html = StringIO(html.encode('utf-8'))
        return self.converter.convert(html)

    def concat(self, pdf, html):
        """Creates a duplicated pdf, from html stream (A.K.A. StringIO)"""

        original = PdfFileReader(StringIO(pdf))

        to_concat = PdfFileReader(StringIO(self.to_pdf(html)))

        out = PdfFileWriter()
        for n in xrange(0, original.getNumPages()):
            out.addPage(original.getPage(n))

        for n in xrange(0, to_concat.getNumPages()):
            out.addPage(to_concat.getPage(n))

        encoded_pdf = StringIO()
        out.write(encoded_pdf)
        encoded_pdf.seek(0)
        encoded_pdf = encoded_pdf.read()

        return encoded_pdf

