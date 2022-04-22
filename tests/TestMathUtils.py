import unittest
import MathUtils


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
        self.assertEqual(MathUtils.Walsh(n=0, t=1, T=1), 1)
        self.assertEqual(MathUtils.Walsh(n=0, t=0, T=1), 1)

        self.assertEqual(MathUtils.Walsh(n=1, t=0.3, T=1), 1)
        self.assertEqual(MathUtils.Walsh(n=1, t=0.6, T=1), -1)

        self.assertEqual(MathUtils.Walsh(n=2, t=0.1, T=1), 1)
        self.assertEqual(MathUtils.Walsh(n=2, t=0.3, T=1), -1)
        self.assertEqual(MathUtils.Walsh(n=2, t=0.6, T=1), -1)
        self.assertEqual(MathUtils.Walsh(n=2, t=0.9, T=1), 1)


if __name__ == "__main__":
    unittest.main()
