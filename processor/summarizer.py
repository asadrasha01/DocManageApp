from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

# Function to generate extractive summary using TextRank
def summarize_text(text, sentence_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))  # Parse text with tokenizer
    summarizer = TextRankSummarizer()  # Create TextRank summarizer instance
    summary = summarizer(parser.document, sentence_count)  # Generate top N summary sentences

    return " ".join(str(sentence) for sentence in summary)  # Join sentences into a single string

# Example usage
def main():
    sample_text = (
        "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. "
        "Leading AI textbooks define the field as the study of intelligent agents: any system that perceives its environment and takes actions that maximize its chance of achieving its goals. "
        "Some popular accounts use the term AI to describe machines that mimic cognitive functions that humans associate with the human mind, such as learning and problem-solving."
    )
    print(summarize_text(sample_text, sentence_count=2))

if __name__ == "__main__":
    main()