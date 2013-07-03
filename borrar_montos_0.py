import models

retiros_con_monto_0 = models.Retiro.select().where(monto=0)

for r in retiros_con_monto_0:
    print "Borrando retiro con monto igual a cero:", r
    r.delete_instance()

