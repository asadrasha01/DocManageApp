from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from transformers import pipeline
from dotenv import load_dotenv
import openai
import re, os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_with_openai(text, max_tokens=150):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize the following text in a clear and concise manner:\n\n{text}"}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except openai.error.OpenAIError as e:
        print(f"Error with OpenAI API: {e}")
        print("Full error details:", e.http_body)
        return f"Error generating summary: {e}"

summarizer = pipeline("summarization", model="google/pegasus-xsum")

def summarize_with_pegasus(text):
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def summarize_text(text, sentence_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

def summarize_with_advanced_model(text):
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def clean_summary(summary):
    summary = re.sub(r'\S+@\S+', '[EMAIL]', summary)
    summary = re.sub(r'\+?[0-9]{1,3}?[-.\s]?[0-9]{1,15}', '[PHONE_NUMBER]', summary)
    technical_terms = ["IP", "subnet", "network", "router", "hardware"]
    for term in technical_terms:
        summary = summary.replace(term, "")
    return summary.strip()

def summarize_document(text, sentence_count=3, use_advanced=False, use_openai=False, use_pegasus=False):
    if use_openai:
        return summarize_with_openai(text)
    elif use_advanced:
        return summarize_with_advanced_model(text)
    elif use_pegasus:
        return summarize_with_pegasus(text)
    return summarize_text(text, sentence_count)

def main():
    sample_text = (
        "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. "
        "Leading AI textbooks define the field as the study of intelligent agents: any system that perceives its environment and takes actions that maximize its chance of achieving its goals. "
        "Some popular accounts use the term AI to describe machines that mimic cognitive functions that humans associate with the human mind, such as learning and problem-solving."
    )
    
    print("\nChatGPT Summary:")
    print(summarize_with_openai(sample_text, max_tokens=150))
    
    print("\nTextRank Summary:")
    print(summarize_document(sample_text, sentence_count=2))
    
    print("\nBART Summary:")
    print(summarize_document(sample_text, sentence_count=2, use_advanced=True))
    
    print("\nPegasus Summary:")
    print(summarize_document(sample_text, sentence_count=2, use_pegasus=True))

if __name__ == "__main__":
    main()