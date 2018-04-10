import unittest
from capstone import util

detector = util.SymbolDetector('data/symlist.txt')

test_sentence1 = 'This is a test for \\alpha and \\beta, see how it works.'
test_sentence2 = 'This is a test for \\a and \\b, see how it works.'

class SymbolDetectorTest(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(detector.detect_symbol(test_sentence1, '\\alpha'), True)
        self.assertEqual(detector.detect_symbol(test_sentence1, '\\beta'), True)

    def test_partial(self):
        self.assertEqual(detector.detect_symbol(test_sentence1, '\\a'), False)
        self.assertEqual(detector.detect_symbol(test_sentence1, '\\b'), False)

    def test_customized(self):
        self.assertEqual(detector.detect_symbol(test_sentence2, '\\a'), True)
        self.assertEqual(detector.detect_symbol(test_sentence2, '\\b'), True)
        self.assertEqual(detector.detect_symbol(test_sentence2, '\\alpha'), False)
        self.assertEqual(detector.detect_symbol(test_sentence2, '\\beta'), False)

if __name__ == '__main__':
    unittest.main()
