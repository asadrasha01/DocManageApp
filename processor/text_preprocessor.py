import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download required NLTK data files (only needed once)
nltk.download('punkt')
nltk.download('stopwords')

# Set of English stopwords for filtering
STOP_WORDS = set(stopwords.words('english'))

# Function to clean and normalize raw text
def clean_text(text):
    text = text.lower()  # Convert text to lowercase
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    return text.strip()  # Remove leading/trailing spaces

# Function to tokenize text into words
def tokenize_text(text):
    return word_tokenize(text)  # Use NLTK's tokenizer

# Function to remove stopwords from a list of tokens
def remove_stopwords(tokens):
    return [word for word in tokens if word not in STOP_WORDS]

# Complete preprocessing pipeline
def preprocess_text(text):
    cleaned = clean_text(text)
    tokens = tokenize_text(cleaned)
    filtered_tokens = remove_stopwords(tokens)
    return filtered_tokens  # Return the final list of tokens

# Example usage
def main():
    raw = "This is a SAMPLE document! It includes punctuation, stopwords, and mixed CASE."
    print(preprocess_text(raw))

if __name__ == "__main__":
    main()
