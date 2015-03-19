import unittest
from time import sleep
from unittest.mock import MagicMock

from bully_async import Bully
from bully_async import BullyFullImpl


class BullyTestCase(unittest.TestCase):
    def test_single(self):
        bully = BullyFullImpl(['http://localhost:11001'], 'http://localhost:11001', ('localhost', 11001) )

        #self.assertFalse(bully.bully.is_master)
        
        sleep(5)
        
        self.assertTrue(bully.bully.is_master)
        
        bully.close()

    def test_1_of_2(self):
        bully1 = BullyFullImpl(['http://localhost:11002','http://localhost:11003'], 'http://localhost:11002', ('localhost', 11002) )
        bully2 = BullyFullImpl(['http://localhost:11002','http://localhost:11003'], 'http://localhost:11003', ('localhost', 11003) )

        sleep(2)
        self.assertTrue(bully1.bully.is_master)

        sleep(2)
        self.assertTrue(bully1.bully.is_master)

        bully1.close()
        bully2.close()


    def test_2_of_3(self):
        bully1 = BullyFullImpl(['http://localhost:11004','http://localhost:11005', 'http://localhost:11006'], 'http://localhost:11004', ('localhost', 11004) )
        bully2 = BullyFullImpl(['http://localhost:11004','http://localhost:11005', 'http://localhost:11006'], 'http://localhost:11005', ('localhost', 11005) )
        bully3 = BullyFullImpl(['http://localhost:11004','http://localhost:11005', 'http://localhost:11006'], 'http://localhost:11006', ('localhost', 11006) )

        sleep(2)
        self.assertTrue(bully1.bully.is_master)
        self.assertFalse(bully2.bully.is_master)

        sleep(2)
        self.assertTrue(bully1.bully.is_master)
        self.assertFalse(bully2.bully.is_master)
        bully1.close()
        sleep(10)

        self.assertTrue(bully2.bully.is_master)
        
        bully2.close()
        bully3.close()

if __name__ == '__main__':
    unittest.main()
