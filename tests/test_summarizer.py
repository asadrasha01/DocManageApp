import unittest
from processor.summarizer import summarize_text

class TestSummarizer(unittest.TestCase):

    def test_summary_length(self):
        text = (
            "Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence. "
            "It is concerned with the interactions between computers and human language. In particular, how to program computers to process and analyze large amounts of natural language data. "
            "Challenges in natural language processing frequently involve natural language understanding, natural language generation, and sentiment analysis."
        )
        summary = summarize_text(text, sentence_count=2)
        self.assertIsInstance(summary, str)
        self.assertTrue(len(summary.split(".")) <= 3)  

    def test_empty_text(self):
        summary = summarize_text("", sentence_count=2)
        self.assertEqual(summary, "")

if __name__ == "__main__":
    unittest.main()