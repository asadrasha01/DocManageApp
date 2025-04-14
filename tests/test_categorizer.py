import unittest
from processor.categorizer import categorize_text

class TestCategorizer(unittest.TestCase):

    def test_finance_keywords(self):
        text = "The bank processed your payment through your account."
        category = categorize_text(text)
        self.assertEqual(category, "Finance")

    def test_legal_keywords(self):
        text = "This agreement is protected under contract law."
        category = categorize_text(text)
        self.assertEqual(category, "Legal")

    def test_education_keywords(self):
        text = "The student attended university and completed their education."
        category = categorize_text(text)
        self.assertEqual(category, "Education")

    def test_llm_fallback(self):
        
        text = "I am excited to join your team as a frontend developer."
        category = categorize_text(text)
        self.assertIsInstance(category, str)
        self.assertNotEqual(category, "Uncategorized")

if __name__ == "__main__":
    unittest.main()