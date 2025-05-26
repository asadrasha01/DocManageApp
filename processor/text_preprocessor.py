import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


STOP_WORDS = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()  
    text = re.sub(r'\s+', ' ', text)  
    text = text.translate(str.maketrans('', '', string.punctuation))  
    return text.strip()  

def tokenize_text(text):
    return word_tokenize(text) 


def remove_stopwords(tokens):
    return [word for word in tokens if word not in STOP_WORDS]

def lemmatize_tokens(tokens):
    return [lemmatizer.lemmatize(word) for word in tokens]

def preprocess_text(text):
    cleaned = clean_text(text)  
    tokens = tokenize_text(cleaned)  
    filtered_tokens = remove_stopwords(tokens) 
    lemmatized_tokens = lemmatize_tokens(filtered_tokens) 
    return lemmatized_tokens 


def main():
    raw = "This is a SAMPLE document! It includes punctuation, stopwords, and mixed CASE."
    print(preprocess_text(raw))

if __name__ == "__main__":
    main()
