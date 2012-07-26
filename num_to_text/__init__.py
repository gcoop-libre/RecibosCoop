#! -*- coding: utf8 -*-

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
#        6:'millon',
#        12:'billon',
#        24:'trillon',
#        48:'cuatrillon', #mas exponentes agregar acá
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

        if number > self.limite:
            msg = "El maximo numero procesable es %s" % self.limite
            raise ValueError(msg)
        else:
            return self.__to_text(number)

    def __to_text(self, number, indice = 0):
            exp = self.exponentes[indice]
            divisor = 10 ** exp
            if divisor < number:
                division = number / divisor
                resto = number % divisor
                der = self._to_text(resto)
                if exp == 3 and division == 1: #1000
                    return "%s %s" % (exponentes[exp], der)
                    izq = ''
                else:
                    izq = self._to_text(division)
                    return "%s %s %s" % (izq, exponentes[exp], der)

            elif divisor == number:
                return exponentes[exp]

            else:
                return self._to_text(number)







    def _to_text(self, number):
        if number <= 15:
            return digitos[number]
        elif number < 20:
            return 'dieci%s' % self.to_text(number%10)

        elif number == 20:
            return 'veinte'

        elif number < 30:
            return 'veinti%s' % self.to_text(number%10)

        elif number < 100:
            texto = decenas[number/10]
            resto = number % 10
            if resto:
                texto += ' y %s' % self.to_text(resto)
            return texto

        if number == 100:
            return 'cien'

        if number < 1000:
            texto = centenas[number/100]
            resto = number % 100
            if resto:
                texto += ' %s' % self.to_text(resto)
            return texto








if __name__ == '__main__':
    t = Traductor()
    print t.to_text(945)




