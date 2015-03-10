import unittest
from count_e import count_e
from count_e_fixed import count_e as count_e_fixed

global ETALON_E

with open("e.txt") as e_file:
    ETALON_E = e_file.readline()

class TestCountE(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(count_e(0), '2.')

    def test_old_in_range_1_350(self):
        for digits in range(1, 350):
            self.assertEqual(count_e(digits)[:-1], ETALON_E[:digits+1], "OLD Test with digits = %d" % digits)

    def test_fixed_in_range_1_350(self):
        for digits in range(1, 350):
            self.assertEqual(count_e_fixed(digits)[:-1], ETALON_E[:digits+1], "FIXED Test with digits = %d" % digits)

    def test_fixed_in_range_350_500(self):
        for digits in range(350, 500):
            self.assertEqual(count_e_fixed(digits)[:-1], ETALON_E[:digits+1], "FIXED Test with digits = %d" % digits)
