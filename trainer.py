import json
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from processor.file_handler import extract_text
from processor.text_preprocessor import preprocess_text

FEEDBACK_FILE = "feedback.json"
MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "doc_classifier.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")
INPUT_DIR = "data/input"

os.makedirs(MODEL_DIR, exist_ok=True)

# Load labeled feedback from feedback.json
def load_training_data():
    if not os.path.exists(FEEDBACK_FILE):
        print("No feedback data available.")
        return pd.DataFrame()

    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        raw_feedback = json.load(f)

    records = []
    for fname, info in raw_feedback.items():
        if info.get("confirmed") and os.path.exists(os.path.join(INPUT_DIR, fname)):
            text = extract_text(os.path.join(INPUT_DIR, fname))
            if not text.startswith("[ERROR]"):
                tokens = preprocess_text(text)
                cleaned = " ".join(tokens)
                records.append({"text": cleaned, "category": info["predicted"]})

    return pd.DataFrame(records)

# Train and save the model
def train_model():
    df = load_training_data()
    if df.empty:
        print("No confirmed feedback data to train on.")
        return

    X = df["text"]
    y = df["category"]

    vectorizer = TfidfVectorizer(max_features=3000)
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_vec, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print("✅ Model trained and saved.")

    # Optional: print classification report (on train set for now)
    y_pred = model.predict(X_vec)
    print("\nTraining report:\n", classification_report(y, y_pred))

if __name__ == "__main__":
    train_model()
