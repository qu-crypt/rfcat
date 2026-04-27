"""Basic import and sanity tests - no hardware required."""
import unittest


class TestImports(unittest.TestCase):
    def test_import_rflib(self):
        import rflib

    def test_import_bits(self):
        from rflib import bits

    def test_fakedongle_importable(self):
        from rflib.fakedongle_nic import FakeRfCat

    def test_fakedongle_instantiates(self):
        from rflib.fakedongle_nic import FakeRfCat
        d = FakeRfCat()
        self.assertIsNotNone(d)

    def test_repr_radio_config(self):
        from rflib.fakedongle_nic import FakeRfCat
        d = FakeRfCat()
        out = d.reprRadioConfig()
        self.assertIsInstance(out, str)
        self.assertIn("Frequency:", out)
