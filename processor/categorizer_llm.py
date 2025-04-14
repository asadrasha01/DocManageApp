from transformers import pipeline


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


LLM_LABELS = [
    "Finance", "Legal", "Education", "Medical", "Technology",
    "HR", "Marketing", "IT Support", "Uncategorized"
]


def llm_categorize(text):
    try:
        result = classifier(text, candidate_labels=LLM_LABELS)
        return result["labels"][0] 
    except Exception as e:
        return f"[LLM ERROR] {e}"