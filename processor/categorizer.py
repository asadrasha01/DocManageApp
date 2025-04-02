import os
from processor.categorizer_ml import ml_categorize, MODEL_READY
from processor.categorizer_llm import llm_categorize

# Define fallback keywords for training or rule backup (optional)
CATEGORY_KEYWORDS = {
    "Finance": ["invoice", "payment", "bank", "account", "finance"],
    "Legal": ["contract", "agreement", "law", "regulation", "legal"],
    "Medical": ["diagnosis", "treatment", "symptom", "medical", "patient"],
    "Education": ["student", "school", "university", "education", "teacher"],
    "Technology": ["software", "hardware", "technology", "AI", "data"],
    "HR": ["resume", "cv", "cover letter", "applicant", "interview", "recruitment"],
    "Marketing": ["marketing", "campaign", "branding", "promotion", "seo"],
    "IT Support": ["ticket", "error", "bug", "issue", "support"]
}

# Hybrid categorization logic
def categorize_text(text):
    text_lower = text.lower()

    # Try ML classifier if available
    if MODEL_READY:
        category = ml_categorize(text_lower)
        if category and not category.startswith("[ML ERROR]"):
            return category

    # Fallback to rule-based categorization
    category_scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            category_scores[category] = score

    if category_scores:
        best_category = max(category_scores, key=category_scores.get)
        return best_category

    # Fallback to zero-shot LLM classification
    return llm_categorize(text)

# Test use
if __name__ == "__main__":
    sample = "I am applying for a backend developer position with my resume."
    print("Predicted category:", categorize_text(sample))
