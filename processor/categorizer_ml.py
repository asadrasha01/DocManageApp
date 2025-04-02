import os
import joblib

MODEL_PATH = "model/doc_classifier.pkl"
VECTORIZER_PATH = "model/vectorizer.pkl"

# Try loading the ML model and vectorizer
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    MODEL_READY = True
except Exception as e:
    print(f"[WARNING] ML model not loaded: {e}")
    model = None
    vectorizer = None
    MODEL_READY = False

# Predict category using trained ML model
def ml_categorize(text):
    if not MODEL_READY:
        return "Uncategorized"

    try:
        vec = vectorizer.transform([text])
        prediction = model.predict(vec)
        return prediction[0]
    except Exception as e:
        return f"[ML ERROR] {e}"
