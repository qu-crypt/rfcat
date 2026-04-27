"""Tests for rflib.bits - no hardware required."""
import unittest
from rflib import bits


class TestCorrectBytes(unittest.TestCase):
    def test_ascii(self):
        self.assertEqual(bits.correctbytes(0x41), b'A')

    def test_zero(self):
        self.assertEqual(bits.correctbytes(0), b'\x00')

    def test_max(self):
        self.assertEqual(bits.correctbytes(0xff), b'\xff')


class TestBitReverse(unittest.TestCase):
    def test_msb_to_lsb(self):
        self.assertEqual(bits.bitReverse(0b10000000, 8), 0b00000001)

    def test_alternating(self):
        self.assertEqual(bits.bitReverse(0b10101010, 8), 0b01010101)

    def test_zero(self):
        self.assertEqual(bits.bitReverse(0, 8), 0)

    def test_all_ones(self):
        self.assertEqual(bits.bitReverse(0xff, 8), 0xff)

    def test_4bit(self):
        self.assertEqual(bits.bitReverse(0b1000, 4), 0b0001)


class TestGetBit(unittest.TestCase):
    def test_msb_of_0x80(self):
        self.assertEqual(bits.getBit(b'\x80', 0), 1)

    def test_lsb_of_0x01(self):
        self.assertEqual(bits.getBit(b'\x01', 7), 1)

    def test_zero_byte(self):
        for i in range(8):
            self.assertEqual(bits.getBit(b'\x00', i), 0)

    def test_second_byte(self):
        self.assertEqual(bits.getBit(b'\x00\x80', 8), 1)


class TestInvertBits(unittest.TestCase):
    def test_ff_becomes_00(self):
        self.assertEqual(bits.invertBits(b'\xff'), b'\x00')

    def test_00_becomes_ff(self):
        self.assertEqual(bits.invertBits(b'\x00'), b'\xff')

    def test_double_invert_identity(self):
        data = b'\xde\xad\xbe\xef'
        self.assertEqual(bits.invertBits(bits.invertBits(data)), data)

    def test_alternating_pattern(self):
        self.assertEqual(bits.invertBits(b'\xaa\x55\xaa\x55'), b'\x55\xaa\x55\xaa')

    def test_four_bytes(self):
        data = b'\x01\x02\x03\x04'
        expected = bytes([b ^ 0xff for b in data])
        self.assertEqual(bits.invertBits(data), expected)


class TestShiftString(unittest.TestCase):
    def test_shift_zero_is_identity(self):
        data = b'\x12\x34\x56'
        self.assertEqual(bits.shiftString(data, 0), data)

    def test_shift_1_single_byte(self):
        # 0x01 << 1 = 0x02
        self.assertEqual(bits.shiftString(b'\x01', 1), b'\x02')

    def test_shift_carries_between_bytes(self):
        # 0x80 0x00 shifted left 1: high bit of first byte carries into second
        result = bits.shiftString(b'\x80\x00', 1)
        self.assertEqual(result[1], 0x00)  # carry was 0x80 >> 7 = 1, but 0x00 << 1 | 1 = 0x01... wait
        # Actually: newc for index 0 = ((0x80 << 1) + (0x00 >> 7)) & 0xff = (0x00 + 0x00) & 0xff = 0x00
        # newc for last byte = (0x00 << 1) & 0xff = 0x00
        self.assertEqual(result, b'\x00\x00')


class TestManchesterCodec(unittest.TestCase):
    def test_roundtrip_hilo1(self):
        for byte_val in (0x00, 0xff, 0xa5, 0x5a, 0xf0):
            data = bytes([byte_val])
            self.assertEqual(bits.manchester_decode(bits.manchester_encode(data, 1), 1), data)

    def test_roundtrip_hilo0(self):
        for byte_val in (0x00, 0xff, 0xa5, 0x5a):
            data = bytes([byte_val])
            self.assertEqual(bits.manchester_decode(bits.manchester_encode(data, 0), 0), data)

    def test_encode_doubles_length(self):
        for n in (1, 2, 4):
            data = bytes(range(n))
            self.assertEqual(len(bits.manchester_encode(data)), 2 * n)

    def test_all_zeros_hilo1_gives_0x5555(self):
        # hilo=1: 0-bit -> lo-hi -> 01, so 0x00 encodes as 0101_0101 0101_0101
        self.assertEqual(bits.manchester_encode(b'\x00', 1), b'\x55\x55')

    def test_all_ones_hilo1_gives_0xaaaa(self):
        # hilo=1: 1-bit -> hi-lo -> 10, so 0xff encodes as 1010_1010 1010_1010
        self.assertEqual(bits.manchester_encode(b'\xff', 1), b'\xaa\xaa')

    def test_all_zeros_hilo0_gives_0xaaaa(self):
        self.assertEqual(bits.manchester_encode(b'\x00', 0), b'\xaa\xaa')

    def test_all_ones_hilo0_gives_0x5555(self):
        self.assertEqual(bits.manchester_encode(b'\xff', 0), b'\x55\x55')


class TestBitSectString(unittest.TestCase):
    def test_full_byte(self):
        data = b'\xa5'
        result, ent = bits.bitSectString(data, 0, 8)
        self.assertEqual(result, b'\xa5')

    def test_entropy_all_zeros_is_low(self):
        _, ent = bits.bitSectString(b'\x00', 0, 8)
        self.assertLess(ent, 0.5)

    def test_entropy_alternating_is_high(self):
        _, ent = bits.bitSectString(b'\xaa\xaa\xaa\xaa', 0, 32)
        self.assertGreater(ent, 0.5)
