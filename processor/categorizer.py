import os
from processor.categorizer_ml import ml_categorize, MODEL_READY
from processor.categorizer_llm import llm_categorize


CATEGORY_KEYWORDS = {
    "Finance": ["invoice", "payment", "bank", "account", "finance", "financial", "investment", "budget"],
    "Legal": ["contract", "agreement", "law", "regulation", "legal", "court", "litigation", "judicial", "attorney"],
    "Medical": ["diagnosis", "treatment", "symptom", "medical", "patient", "hospital", "healthcare", "doctor", "nurse"],
    "Education": ["student", "school", "university", "education", "teacher", "classroom", "academic", "research"],
    "Technology": ["software", "hardware", "technology", "AI", "data", "networking", "IP", "subnet", "router", "protocol", "cloud", "computing"],
    "HR": ["resume", "cv", "cover letter", "applicant", "interview", "recruitment", "job", "employee", "candidate"],
    "Marketing": ["marketing", "campaign", "branding", "promotion", "seo", "advertisement", "target audience", "social media"],
    "IT Support": ["ticket", "error", "bug", "issue", "support", "helpdesk", "troubleshooting", "system admin", "service"]
}

CATEGORY_CONFIDENCE_THRESHOLD = 2 

def categorize_text(text):
    text_lower = text.lower()

    if MODEL_READY:
        category = ml_categorize(text_lower)
        if category and not category.startswith("[ML ERROR]"):
            return category  

    category_scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score >= CATEGORY_CONFIDENCE_THRESHOLD: 
            category_scores[category] = score

    if category_scores:
        best_category = max(category_scores, key=category_scores.get)
        return best_category

    return llm_categorize(text)


if __name__ == "__main__":
    sample = "I am applying for a backend developer position with my resume."
    print("Predicted category:", categorize_text(sample))
