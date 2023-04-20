import unittest
from config import Config
from util import ping

class TestConfig(unittest.TestCase):
    
    def setUp(self):
        self.config = Config()
        
    def test_load_file_config(self):
        config = self.config._load_json()
        
        self.assertEqual(type(config), type({}))
    
    def test_lista_computadores(self):
        esperado = 2
        computadores = self.config.get_computadores()
        
        self.assertEqual(esperado, len(computadores))
        
        
class TestUtil(unittest.TestCase):
    
    def test_ping_ok(self):
        resposta = ping('192.168.20.199')
        
        self.assertEqual(0, int(resposta))
        
    def test_ping_error(self):
        resposta = ping('192.168.20.250')
        
        self.assertNotEqual(int(resposta), 0)
        
    