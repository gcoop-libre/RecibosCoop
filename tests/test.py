import sys
sys.path.append("..")
sys.path.append(".")

import os
import app
import deploy
import unittest
import tempfile
import models

class RecibosTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_acceso_aplicacion(self):
        rv = self.app.get('/')
        self.assertTrue('Gcoop' in rv.data)

    def test_nombres_de_los_socios(self):
        socios = models.Socio.select().where()
        nombres = [x.nombre for x in socios]
        self.assertTrue('Pepe' in nombres)

if __name__ == '__main__':
    deploy.crear_tablas()
    deploy.cargar_fixture_2_usuarios()
    unittest.main()
