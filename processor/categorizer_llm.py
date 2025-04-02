from transformers import pipeline

# Load the zero-shot classification model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# List of candidate categories
LLM_LABELS = [
    "Finance", "Legal", "Education", "Medical", "Technology",
    "HR", "Marketing", "IT Support", "Uncategorized"
]

# Fallback classifier using transformers (LLM)
def llm_categorize(text):
    try:
        result = classifier(text, candidate_labels=LLM_LABELS)
        return result["labels"][0]  # return the most likely label
    except Exception as e:
        return f"[LLM ERROR] {e}"