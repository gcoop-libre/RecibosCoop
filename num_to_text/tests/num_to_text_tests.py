#! -*- coding: utf8 -*-

import unittest
import num_to_text
from decimal import Decimal

class TestTraductorNumeros(unittest.TestCase):
    def setUp(self):
        self.trad = num_to_text.Traductor()

    def test_digitos(self):
        self.assertEquals(self.trad.to_text(0), 'cero')
        self.assertEquals(self.trad.to_text(1), 'uno')
        self.assertEquals(self.trad.to_text(2), 'dos')
        self.assertEquals(self.trad.to_text(3), 'tres')
        self.assertEquals(self.trad.to_text(4), 'cuatro')
        self.assertEquals(self.trad.to_text(5), 'cinco')
        self.assertEquals(self.trad.to_text(6), 'seis')
        self.assertEquals(self.trad.to_text(7), 'siete')
        self.assertEquals(self.trad.to_text(8), 'ocho')
        self.assertEquals(self.trad.to_text(9), 'nueve')

    def test_decenas(self):
        self.assertEquals(self.trad.to_text(10), 'diez')
        self.assertEquals(self.trad.to_text(11), 'once')
        self.assertEquals(self.trad.to_text(12), 'doce')
        self.assertEquals(self.trad.to_text(13), 'trece')
        self.assertEquals(self.trad.to_text(14), 'catorce')
        self.assertEquals(self.trad.to_text(15), 'quince')
        self.assertEquals(self.trad.to_text(16), 'dieciseis')
        self.assertEquals(self.trad.to_text(17), 'diecisiete')
        self.assertEquals(self.trad.to_text(18), 'dieciocho')
        self.assertEquals(self.trad.to_text(19), 'diecinueve')
        self.assertEquals(self.trad.to_text(20), 'veinte')
        self.assertEquals(self.trad.to_text(21), 'veintiuno')
        self.assertEquals(self.trad.to_text(22), 'veintidos')
        self.assertEquals(self.trad.to_text(23), 'veintitres')
        self.assertEquals(self.trad.to_text(24), 'veinticuatro')
        self.assertEquals(self.trad.to_text(25), 'veinticinco')
        self.assertEquals(self.trad.to_text(26), 'veintiseis')
        self.assertEquals(self.trad.to_text(27), 'veintisiete')
        self.assertEquals(self.trad.to_text(28), 'veintiocho')
        self.assertEquals(self.trad.to_text(29), 'veintinueve')
        self.assertEquals(self.trad.to_text(30), 'treinta')
        self.assertEquals(self.trad.to_text(37), 'treinta y siete')
        self.assertEquals(self.trad.to_text(40), 'cuarenta')
        self.assertEquals(self.trad.to_text(42), 'cuarenta y dos')
        self.assertEquals(self.trad.to_text(50), 'cincuenta')
        self.assertEquals(self.trad.to_text(55), 'cincuenta y cinco')
        self.assertEquals(self.trad.to_text(60), 'sesenta')
        self.assertEquals(self.trad.to_text(66), 'sesenta y seis')
        self.assertEquals(self.trad.to_text(70), 'setenta')
        self.assertEquals(self.trad.to_text(77), 'setenta y siete')
        self.assertEquals(self.trad.to_text(80), 'ochenta')
        self.assertEquals(self.trad.to_text(88), 'ochenta y ocho')
        self.assertEquals(self.trad.to_text(90), 'noventa')
        self.assertEquals(self.trad.to_text(99), 'noventa y nueve')

    def test_centenas(self):
        self.assertEquals(self.trad.to_text(100), 'cien')
        self.assertEquals(self.trad.to_text(111), 'ciento once')
        self.assertEquals(self.trad.to_text(200), 'doscientos')
        self.assertEquals(self.trad.to_text(222), 'doscientos veintidos')
        self.assertEquals(self.trad.to_text(300), 'trescientos')
        self.assertEquals(self.trad.to_text(333), 'trescientos treinta y tres')
        self.assertEquals(self.trad.to_text(400), 'cuatrocientos')
        self.assertEquals(self.trad.to_text(444), 'cuatrocientos cuarenta y cuatro')
        self.assertEquals(self.trad.to_text(500), 'quinientos')
        self.assertEquals(self.trad.to_text(555), 'quinientos cincuenta y cinco')
        self.assertEquals(self.trad.to_text(600), 'seiscientos')
        self.assertEquals(self.trad.to_text(666), 'seiscientos sesenta y seis')
        self.assertEquals(self.trad.to_text(700), 'setecientos')
        self.assertEquals(self.trad.to_text(777), 'setecientos setenta y siete')
        self.assertEquals(self.trad.to_text(800), 'ochocientos')
        self.assertEquals(self.trad.to_text(888), 'ochocientos ochenta y ocho')
        self.assertEquals(self.trad.to_text(900), 'novecientos')
        self.assertEquals(self.trad.to_text(953), 'novecientos cincuenta y tres')
        self.assertEquals(self.trad.to_text(999), 'novecientos noventa y nueve')

    def test_miles(self):
        self.assertEquals(self.trad.to_text(7532), 'siete mil quinientos treinta y dos')
        self.assertEquals(self.trad.to_text(1014), 'mil catorce')
        self.assertEquals(self.trad.to_text(21000), 'veintiun mil')
        self.assertEquals(self.trad.to_text(71000), 'setenta y un mil')

        self.assertEquals(self.trad.to_text(916543), 'novecientos dieciseis mil quinientos cuarenta y tres')

    def test_numeros_grandes(self):
        self.assertEquals(self.trad.to_text(1000000), 'un millon');
        self.assertEquals(self.trad.to_text(1000021), 'un millon veintiuno');
        self.assertEquals(self.trad.to_text(41000021), 'cuarenta y un millones veintiuno');
        self.assertEquals(self.trad.to_text(41000021), 'cuarenta y un millones veintiuno');

        self.assertEquals(self.trad.to_text(416010015), 'cuatrocientos dieciseis millones diez mil quince');
        self.assertEquals(self.trad.to_text(1123123123123123123123123123123123456123456), 'un millon ciento veintitres mil ciento veintitres billones ciento veintitres mil ciento veintitres millones ciento veintitres mil ciento veintitres trillones ciento veintitres mil ciento veintitres millones ciento veintitres mil ciento veintitres billones ciento veintitres mil cuatrocientos cincuenta y seis millones ciento veintitres mil cuatrocientos cincuenta y seis');

    def test_decimales(self):
        self.assertEquals(self.trad.to_text(16.1), 'dieciseis con 10/100')
        self.assertEquals(self.trad.to_text(16.321), 'dieciseis con 32/100')
        self.assertEquals(self.trad.to_text(Decimal('1123123123123123123123123123123123456123456.33')), 'un millon ciento veintitres mil ciento veintitres billones ciento veintitres mil ciento veintitres millones ciento veintitres mil ciento veintitres trillones ciento veintitres mil ciento veintitres millones ciento veintitres mil ciento veintitres billones ciento veintitres mil cuatrocientos cincuenta y seis millones ciento veintitres mil cuatrocientos cincuenta y seis con 33/100');



if __name__ == '__main__':

    unittest.main()

