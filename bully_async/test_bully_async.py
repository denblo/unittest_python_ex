import unittest
from time import sleep
from unittest.mock import MagicMock

from bully_async import Bully
from bully_async import BullyFullImpl


class BullyTestCase(unittest.TestCase):
    def test_single(self):
        m = MagicMock()
        bully = BullyFullImpl(['http://localhost:11001'], 'http://localhost:11001', ('localhost', 11001) )
        self.assertFalse(bully.bully.is_master)
        
        sleep(5)
        
        self.assertTrue(bully.bully.is_master)
        
        bully.close()
        

    # def test_1_of_2(self):
    #     m = MagicMock(side_effect=lambda a, b: True)
    #     bully = Bully(['me', 'that_guy'], 'me', m)
    #     self.assertFalse(bully.is_master)
    #     bully.on_tick()
    #     self.assertTrue(bully.is_master)
    #     self.assertEqual(m.call_count, 0)
    #     bully.on_tick()
    #     self.assertEqual(m.call_count, 1)
    #     m.assert_called_with(['that_guy'], 0)
    #     self.assertTrue(bully.on_bully(1))
    #     bully.on_tick()
    #     self.assertEqual(m.call_count, 2)
    #     self.assertTrue(bully.is_master)


    # def test_2_of_3(self):
    #     m = MagicMock(side_effect=lambda a, b: True)
    #     bully = Bully(['that_guy', 'me', 'another_one'], 'me', m)
    #     self.assertFalse(bully.is_master)
    #     bully.on_tick()
    #     self.assertFalse(bully.is_master)
    #     bully.on_tick()
    #     self.assertFalse(bully.is_master)
    #     self.assertTrue(bully.on_bully(2))


    #     for i in range(Bully.TICKS_BEFORE_BULLYING):
    #         self.assertFalse(bully.is_master)
    #         bully.on_tick()
    #     self.assertTrue(bully.is_master)
    #     self.assertFalse(bully.on_bully(0))
    #     self.assertFalse(bully.is_master)




if __name__ == '__main__':
    unittest.main()
