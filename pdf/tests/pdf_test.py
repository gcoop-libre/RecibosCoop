import unittest
from pdf import Pdf

class TestObjetoPDF(unittest.TestCase):

    def setUp(self):
        pass

    def assertPdfEquals(self, a, b):
        """Utility Function to test pdf equality"""
        return self.assertEquals(a.splitlines()[7:], b.splitlines()[7:]);

    def test_get_stream_single(self):
        first_html = "<h1>Hola Mundo</h1>"
        pdf = Pdf(first_html)
        fh = open('tests/fixtures/hola_mundo.pdf', 'rb')
        data = fh.read()
        fh.close()
        output = pdf.get_stream()
        self.assertPdfEquals(output, data)

    def test_get_stream(self):
        first_html = "<h1>Hola Mundo</h1>"
        second_html = "<h2>This is sparta</h2>"
        pdf = Pdf(first_html)
        pdf.append(second_html)
        fh = open('tests/fixtures/stream.pdf', 'rb')
        data = fh.read()
        fh.close()
        output = pdf.get_stream()
        self.assertPdfEquals(output, data)

    def test_append(self):
        first_html = "<h1>Hola Mundo</h1>"
        second_html = "<h2>This is sparta</h2>"
        pdf = Pdf(first_html)
        pdf.append(second_html)
        self.assertEquals(pdf.htmls, [first_html, second_html])

    def test_to_pdf(self):
        first_html = "<h1>Hola Mundo</h1>"
        pdf = Pdf(first_html)
        fh = open('tests/fixtures/hola_mundo.pdf', 'rb')
        data = fh.read()
        fh.close()
        output = pdf.to_pdf(first_html)
        self.assertPdfEquals(output, data)

    def test_concat(self):
        first_html = "<h1>Hola Mundo</h1>"
        second_html = "<h2>This is sparta</h2>"
        pdf = Pdf(first_html)
        output = pdf.concat(pdf.get_stream(), second_html)

        fh = open('tests/fixtures/concat.pdf', 'rb')
        data = fh.read()
        fh.close()

        self.assertPdfEquals(output, data);



