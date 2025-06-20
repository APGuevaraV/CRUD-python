import unittest
import config
import csv
import database as db
import copy
import helpers

class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        db.Clientes.lista = [
            db.Cliente('15J','Martha', 'Perez'),
            db.Cliente('48H','Juana','Carrera'),
            db.Cliente('58P','Paola','Ruiz')
        ]
        
    def test_buscar_cliente(self):
        cliente_existente = db.Clientes.buscar('15J')
        cliente_inexistente = db.Clientes.buscar('18M')
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)
        
    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear('39X','Ana','Guevara')
        self.assertEqual(len(db.Clientes.lista),4)
        self.assertEqual(nuevo_cliente.dni,'39X')
        self.assertEqual(nuevo_cliente.nombre,'Ana')
        self.assertEqual(nuevo_cliente.apellido,'Guevara')
        
    def test_modificar_cliente(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar('15J'))
        cliente_modificado = db.Clientes.modificar('15J','Mariana','Garcia')
        self.assertEqual(cliente_a_modificar.nombre,'Martha')
        self.assertEqual(cliente_modificado.nombre,'Mariana')
        
    def test_borrar_cliente(self):
        cliente_a_borrar = copy.copy(db.Clientes.borrar('15J'))
        cliente_buscado = db.Clientes.buscar('15J')
        self.assertEqual(cliente_a_borrar.nombre,'Martha')
        self.assertIsNone(cliente_buscado)
        
    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido('12X',db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('15J',db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('AJ',db.Clientes.lista))
        
    def test_escritura(self):
        db.Clientes.borrar('48H')
        db.Clientes.borrar('15J')
        db.Clientes.modificar('58P','Maria','Reyes')
        
        dni,nombre,apellido = None, None, None
        with open(config.DATABASE_PATH,newline='\n') as fichero:
            reader = csv.reader(fichero,delimiter=';')
            dni,nombre, apellido = next(reader)
            
            
        self.assertEqual(dni,'58P')
        self.assertEqual(nombre,'Maria')
        self.assertEqual(apellido,'Reyes')
        