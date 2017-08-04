#!/usr/bin/env python3

import unittest

from witch import WVec


class TestWVec(unittest.TestCase):

    def test_WVec_init(self):

        a = WVec(22)
        a = WVec('1010101')
        a = WVec([0, 1, 1, 0])
        a = WVec([True, True, False, True])
        a = WVec(['0', '1', '0', '1'])
        a = WVec([1, False, True, '0', '1', 0])

        try:
            a = WVec('hat')
            self.assertTrue(False)
        except ValueError:
            pass

        try:
            a = WVec([1, '0', 'a'])
            self.assertTrue(False)
        except ValueError:
            pass

        try:
            a = WVec([1, '0', 'string'])
            self.assertTrue(False)
        except ValueError:
            pass

        a = WVec("1100", length=10, signed=True)

        self.assertEqual(a, "1111111100")

        a = WVec("0100", length=10, signed=True)

        self.assertEqual(a, "0000000100")

        try:
            a = WVec('010100a')
            self.assertTrue(False)
        except ValueError:
            pass

    def test_getitem(self):

        a = WVec(0)

        self.assertEqual(a[0], False)

        self.assertEqual(len(a), 1)

        try:
            self.assertEqual(a[1], -5000)
        except IndexError:
            pass

        a = WVec(4)

        self.assertEqual(a, [False, False, True])
        self.assertEqual(a, 4)
        self.assertEqual(a, '100')

    def test_tostring(self):

        a = WVec(10)

        self.assertEqual(a.__str__(), '1010')

    def test_int(self):

        a = WVec(-22)

        self.assertEqual(a, -22)

        a = WVec(10)

        self.assertEqual(a, 10)

    def test_add(self):

        a = WVec(10)
        b = WVec(22)

        c = a + b

        self.assertEqual(c, 32)

        a = WVec(0xdeadbeef)
        b = WVec(0xbaadf00d)

        self.assertEqual(a + b, 0xdeadbeef+0xbaadf00d)

    def test_sub(self):

        a = WVec(49)
        b = WVec(22)

        self.assertEqual(a - b, 27)

    def test_or(self):

        a = WVec(0xdeadbeef)
        b = WVec(0xbaadf00d)

        self.assertEqual(a | b, 0xfeadfeef)

    def test_and(self):

        a = WVec(0xdeadbeef)
        b = WVec(0xbaadf00d)

        self.assertEqual(a & b, 0x9aadb00d)

    def test_xor(self):

        a = WVec(0xdeadbeef)
        b = WVec(0xbaadf00d)

        c = a ^ b

        self.assertEqual(c, 0x64004ee2)

    def test_invert(self):

        a = WVec('1100110011')

        self.assertEqual(~a, '0011001100')

    pass

# End of file
