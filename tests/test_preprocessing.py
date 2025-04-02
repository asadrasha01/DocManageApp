import unittest
from processor.text_preprocessor import preprocess_text

class TestTextPreprocessing(unittest.TestCase):

    def test_removes_punctuation_and_lowercases(self):
        text = "Hello, World! This is a Test."
        tokens = preprocess_text(text)
        self.assertIn("hello", tokens)
        self.assertIn("world", tokens)
        self.assertNotIn("Hello", tokens)
        self.assertNotIn(",", tokens)

    def test_removes_stopwords(self):
        text = "This is a simple sentence."
        tokens = preprocess_text(text)
        self.assertNotIn("is", tokens)
        self.assertNotIn("a", tokens)
        self.assertIn("simple", tokens)
        self.assertIn("sentence", tokens)

    def test_handles_empty_input(self):
        tokens = preprocess_text("")
        self.assertEqual(tokens, [])

if __name__ == "__main__":
    unittest.main()
