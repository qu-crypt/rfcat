"""Tests against FakeRfCat and IntelHex - no hardware required."""
import os
import tempfile
import unittest


class TestFakeRfCat(unittest.TestCase):
    def setUp(self):
        from rflib.fakedongle_nic import FakeRfCat
        self.d = FakeRfCat()

    def test_repr_radio_config_returns_string(self):
        out = self.d.reprRadioConfig()
        self.assertIsInstance(out, str)

    def test_set_get_freq(self):
        self.d.setFreq(433920000)
        freq, _ = self.d.getFreq()
        self.assertAlmostEqual(freq, 433920000, delta=10000)

    def test_set_get_drate(self):
        self.d.setMdmDRate(38400)
        rate = self.d.getMdmDRate()
        self.assertAlmostEqual(rate, 38400, delta=500)

    def test_set_modulation_ook(self):
        from rflib.const import MOD_ASK_OOK
        self.d.setMdmModulation(MOD_ASK_OOK)
        mod = self.d.getMdmModulation()
        self.assertEqual(mod, MOD_ASK_OOK)

    def test_make_pkt_fixed_len(self):
        self.d.makePktFLEN(32)
        length, _ = self.d.getPktLEN()
        self.assertEqual(length, 32)

    def test_ping(self):
        result = self.d.ping()
        self.assertTrue(result)


class TestIntelHex(unittest.TestCase):
    def test_puts_gets_roundtrip(self):
        from rflib.intelhex import IntelHex
        ih = IntelHex()
        data = b'hello world' * 10
        ih.puts(0, data)
        self.assertEqual(ih.gets(0, len(data)), data)

    def test_write_read_hex_file(self):
        from rflib.intelhex import IntelHex
        data = b'hello world' * 100
        ih = IntelHex()
        ih.puts(0, data)
        with tempfile.NamedTemporaryFile(suffix='.hex', delete=False) as f:
            path = f.name
        try:
            ih.write_hex_file(path)
            ih2 = IntelHex()
            ih2.loadhex(path)
            self.assertEqual(ih2.gets(0, len(data)), data)
        finally:
            os.unlink(path)

    def test_min_max_addr(self):
        from rflib.intelhex import IntelHex
        ih = IntelHex()
        ih.puts(0x1000, b'\xde\xad\xbe\xef')
        self.assertEqual(ih.minaddr(), 0x1000)
        self.assertEqual(ih.maxaddr(), 0x1003)

    def test_tobinstr(self):
        from rflib.intelhex import IntelHex
        ih = IntelHex()
        ih.puts(0, b'\x01\x02\x03')
        result = ih.tobinstr(start=0, end=2)
        self.assertEqual(result, b'\x01\x02\x03')

    def test_from_dict(self):
        from rflib.intelhex import IntelHex
        ih = IntelHex({0: 0xde, 1: 0xad, 2: 0xbe, 3: 0xef})
        self.assertEqual(ih.gets(0, 4), b'\xde\xad\xbe\xef')


class TestImportingDongle(unittest.TestCase):
    """Requires a hardware dongle attached. Errors without one (expected)."""
    def test_importing(self):
        import rflib
        rflib.RfCat(idx=0)
