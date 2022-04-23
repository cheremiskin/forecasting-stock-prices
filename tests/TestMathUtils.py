import math
import unittest
import MathUtils
from GrayCodeBuilder import GrayCodeBuilder


class TestMathUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.gray_code_builder = GrayCodeBuilder(math.ceil(math.log2(40)))

    def test_sign(self):
        self.assertEqual(MathUtils.sign(0), 0)
        self.assertEqual(MathUtils.sign(-5), -1)
        self.assertEqual(MathUtils.sign(5), 1)

    def test_Rad(self):
        self.assertEqual(MathUtils.Rad(n=0, t=0), 0)
        self.assertEqual(MathUtils.Rad(n=1, t=0.3), 1)
        self.assertEqual(MathUtils.Rad(n=1, t=0.6), -1)
        self.assertEqual(MathUtils.Rad(n=2, t=0.3), -1)
        self.assertEqual(MathUtils.Rad(n=2, t=0.6), 1)

    def test_Walsh(self):
        self.assertEqual(
            MathUtils.Walsh(n=0, t=0, gray_code_builder=self.gray_code_builder), 1
        )
        self.assertEqual(
            MathUtils.Walsh(n=0, t=0.5, gray_code_builder=self.gray_code_builder), 1
        )
        self.assertEqual(
            MathUtils.Walsh(n=0, t=0.9, gray_code_builder=self.gray_code_builder), 1
        )
        self.assertEqual(
            MathUtils.Walsh(n=1, t=0.5, gray_code_builder=self.gray_code_builder), 1
        )


if __name__ == "__main__":
    unittest.main()
