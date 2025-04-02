import json
import os

FEEDBACK_FILE = "feedback.json"

# Load existing feedback from file (if available)
def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Save feedback to file
def save_feedback(feedback):
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedback, f, indent=4, ensure_ascii=False)

# Ask user for confirmation and save result
def ask_user_feedback(filename, predicted_category):
    print(f"\nPredicted category for '{filename}' is: {predicted_category}")
    feedback = input("Is this correct? (y/n): ").strip().lower()
    return feedback == 'y'

# Update feedback record
def record_feedback(filename, predicted_category, confirmed):
    feedback_data = load_feedback()
    feedback_data[filename] = {
        "predicted": predicted_category,
        "confirmed": confirmed
    }
    save_feedback(feedback_data)

# Example usage
def main():
    sample_file = "test_doc.pdf"
    category = "Finance"
    confirmed = ask_user_feedback(sample_file, category)
    record_feedback(sample_file, category, confirmed)

if __name__ == "__main__":
    main()
