import unittest
import MathUtils
from GrayCodeBuilder import GrayCodeBuilder


class TestMathUtils(unittest.TestCase):
    def test_sign(self):
        self.assertEqual(MathUtils.sign(0), 0)
        self.assertEqual(MathUtils.sign(-5), -1)
        self.assertEqual(MathUtils.sign(5), 1)

    def test_Rad(self):
        self.assertEqual(MathUtils.Rad(n=0, t=0), 1)
        self.assertEqual(MathUtils.Rad(n=1, t=0.3), 1)
        self.assertEqual(MathUtils.Rad(n=1, t=0.6), -1)
        self.assertEqual(MathUtils.Rad(n=2, t=0.3), -1)
        self.assertEqual(MathUtils.Rad(n=2, t=0.6), 1)

    def test_Walsh(self):
        pass


if __name__ == "__main__":
    unittest.main()
