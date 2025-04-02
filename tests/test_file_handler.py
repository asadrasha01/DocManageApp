import unittest
import os
from processor.file_handler import extract_text

TEST_DIR = "tests/resources"

class TestFileHandler(unittest.TestCase):

    def setUp(self):
        os.makedirs(TEST_DIR, exist_ok=True)
        # Create a simple .txt file
        with open(os.path.join(TEST_DIR, "sample.txt"), "w", encoding="utf-8") as f:
            f.write("This is a test document for text extraction.")

    def test_txt_extraction(self):
        path = os.path.join(TEST_DIR, "sample.txt")
        result = extract_text(path)
        self.assertIn("test document", result)

    def test_unsupported_format(self):
        path = os.path.join(TEST_DIR, "sample.unsupported")
        with open(path, "w", encoding="utf-8") as f:
            f.write("irrelevant")
        result = extract_text(path)
        self.assertTrue(result.startswith("[ERROR]"))

    def tearDown(self):
        for file in os.listdir(TEST_DIR):
            os.remove(os.path.join(TEST_DIR, file))
        os.rmdir(TEST_DIR)

if __name__ == "__main__":
    unittest.main()
