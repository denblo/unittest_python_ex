import unittest
from unittest.mock import MagicMock

from bully import Bully


class BullyTestCase(unittest.TestCase):

    def test_index(self):
        bully = Bully(['me', 'notme'], 'me', None)
        self.assertEqual(bully.index, 0)

        bully = Bully(['notme','me', 'notme2'], 'me', None)
        self.assertEqual(bully.index, 1)

    def test_single(self):
        bully = Bully(['me'], 'me', None)
        for i in range(bully.TICKS_BEFORE_BULLYING + 1):
            self.assertFalse(bully.is_master)
            bully.on_tick()
        self.assertTrue(bully.is_master)

        self.assertRaises(AssertionError, Bully,['Oh shit!'], 'me', None)

    def test_communicate_master(self):
        m = MagicMock(side_effect=lambda target, im: True)
        bully = Bully(['me', 'that_guy'], 'me', m)
        for i in range(bully.TICKS_BEFORE_BULLYING):
            self.assertFalse(bully.is_master)
            bully.on_tick()

        self.assertFalse(bully.is_master)
        self.assertEqual(m.call_count, 0)

        bully.on_tick()
        self.assertTrue(bully.is_master)

        bully.on_tick()
        self.assertTrue(bully.is_master)
        self.assertEqual(m.call_count, 1)

        self.assertTrue(bully.is_master)


    def test_communicate_slave(self):
        m = MagicMock(side_effect=lambda target, im: True)
        bully = Bully(['that_guy', 'me', 'other_guy'], 'me', m)

        for i in range(bully.TICKS_BEFORE_BULLYING):
            self.assertFalse(bully.is_master)
            bully.on_tick()

        self.assertFalse(bully.is_master)
        self.assertEqual(m.call_count, 0)

        bully.on_tick()
        self.assertFalse(bully.is_master)
        self.assertEqual(m.call_count, 1)

        bully.on_tick()
        self.assertFalse(bully.is_master)
        self.assertEqual(m.call_count, 2)

if __name__ == '__main__':
    unittest.main()
