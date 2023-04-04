import unittest
from mermaid_to_bugs import translate_v2

class TestStringMethods(unittest.TestCase):

    def test_1(self):

        self.assertEqual(translate_v2("Node1:constant[0.5]\nNode2:constant[8]\nNode1, Node2--> Node3:stochastic[dbin]\nNode3 --> Node4:logical[step]"), "YES")


if __name__ == '__main__':
    unittest.main()