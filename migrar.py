import sqlite3

con = sqlite3.connect('recibos.db')
cur = con.cursor()
try:
    cur.execute('alter table retiro add column concepto char(255)')
    print "Agregando la columna 'concepto' a la tabla retiro."
except:
    pass

print "Definiendo un valor inicial para todos los conceptos."
cur.execute("update retiro set concepto='anticipo de retornos a cuenta de excedentes'")
con.commit()
con.close()
