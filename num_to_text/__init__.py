#! -*- coding: utf8 -*-
from decimal import Decimal

digitos = [
        'cero',
        'uno',
        'dos',
        'tres',
        'cuatro',
        'cinco',
        'seis',
        'siete',
        'ocho',
        'nueve',
        'diez',
        'once',
        'doce',
        'trece',
        'catorce',
        'quince',
        ]

decenas = [
        '',
        'diez',
        'veinte',
        'treinta',
        'cuarenta',
        'cincuenta',
        'sesenta',
        'setenta',
        'ochenta',
        'noventa',
        ]

centenas = [
        '',
        'ciento',
        'doscientos',
        'trescientos',
        'cuatrocientos',
        'quinientos',
        'seiscientos',
        'setecientos',
        'ochocientos',
        'novecientos',
        ]

exponentes = {
#        2:'cien',
        3:'mil',
        6:'millon',
        12:'billon',
        24:'trillon',
        48:'cuatrillon', #mas exponentes agregar acá
    }

class Traductor(object):

    def __init__(self):
        self.calcular_limite()

    def calcular_limite(self):
        """
        Calcula el numero maximo que se puede imprimir
        """
        self.exponentes = sorted(exponentes.keys(), reverse=True)
        exp = self.exponentes[0]
        self.limite = 10 ** (exp*2) - 1

    def to_text(self, number):
        """Interfaz publica para convertir numero a texto"""

        if type(number) != Decimal:
            number = Decimal(number)

        if number > self.limite:
            msg = "El maximo numero procesable es %s" % self.limite
            raise ValueError(msg)
        else:
            texto = self.__to_text(int(number))
        texto += self.__calcular_decimales(number)

        return texto

    def __calcular_decimales(self, number):
        dec = number.remainder_near(1)
        if  dec != 0:
            centavos = int(dec * 100)
            return ' con %s/100' % centavos
        else:
            return ''

    def __to_text(self, number, indice = 0):
        """Convierte un numero a texto, recursivamente"""

        exp = self.exponentes[indice]
        indice += 1
        divisor = 10 ** exp
        if exp == 3:
            func = self.__numero_tres_cifras
        else:
            func = self.__to_text
        if divisor < number:
            division = number / divisor
            resto = number % divisor
            der = func(resto, indice)
            if exp == 3 and division == 1: #1000
                return "%s %s" % (exponentes[exp], der)
                izq = ''
            else:
                izq = func(division, indice)
                if division == 1:
                    return "un %s %s" % (exponentes[exp], der)
                elif exp > 3:
                    return "%s %ses %s" % (izq, exponentes[exp], der)
                else:
                    return "%s %s %s" % (izq, exponentes[exp], der)

        elif divisor == number:
            if exp == 3:
                return exponentes[exp]
            else:
                return 'un %s' % exponentes[exp]

        else:
            return func(number, indice)

    def __numero_tres_cifras(self, number, indice=None):
        """Convierte a texto numeros de tres cifras"""

        if number <= 15:
            return digitos[number]
        elif number < 20:
            return 'dieci%s' % self.__numero_tres_cifras(number%10)

        elif number == 20:
            return 'veinte'

        elif number < 30:
            return 'veinti%s' % self.__numero_tres_cifras(number%10)

        elif number < 100:
            texto = decenas[number/10]
            resto = number % 10
            if resto:
                texto += ' y %s' % self.__numero_tres_cifras(resto)
            return texto

        if number == 100:
            return 'cien'

        if number < 1000:
            texto = centenas[number/100]
            resto = number % 100
            if resto:
                texto += ' %s' % self.__numero_tres_cifras(resto)
            return texto








if __name__ == '__main__':
    t = Traductor()
    print t.to_text(1000000)




