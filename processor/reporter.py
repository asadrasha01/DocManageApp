import os
import pandas as pd
from fpdf import FPDF
from config import FONT_PATH

# Function to save data to CSV format
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# Function to save data to Excel format
def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

# Function to sanitize text for PDF rendering
def sanitize_text(text):
    if not isinstance(text, str):
        return ""
    # Remove characters that can't be encoded
    return text.encode("latin1", errors="replace").decode("latin1")

# Function to save data to PDF format
def save_to_pdf(data, filename):
    pdf = FPDF()
    pdf.add_page()
    try:
        pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
        pdf.set_font("DejaVu", size=12)
    except Exception as e:
        print(f"[ERROR] Could not load font: {e}")
        pdf.set_font("Arial", size=12)

    for item in data:
        try:
            fname = sanitize_text(item.get("filename", ""))
            category = sanitize_text(item.get("category", "Uncategorized"))
            summary = sanitize_text(item.get("summary", ""))

            # Ensure all fields are printable
            if not fname or not category:
                continue

            line = f"Filename: {fname}\nCategory: {category}\nSummary: {summary}\n"
            pdf.multi_cell(0, 10, line + "\n------------------------\n")
        except Exception as e:
            print(f"[ERROR] Skipping entry due to: {e}")
            continue

    try:
        pdf.output(filename)
    except Exception as e:
        print(f"[ERROR] Failed to write PDF: {e}")

# Example usage
def main():
    sample_data = [
        {"filename": "doc1.pdf", "category": "Finance", "summary": "Bank account and payment details."},
        {"filename": "doc2.docx", "category": "Education", "summary": "University courses and schedules."}
    ]

    from config import OUTPUT_DIR
    save_to_csv(sample_data, os.path.join(OUTPUT_DIR, "report.csv"))
    save_to_excel(sample_data, os.path.join(OUTPUT_DIR, "report.xlsx"))
    save_to_pdf(sample_data, os.path.join(OUTPUT_DIR, "report.pdf"))

if __name__ == "__main__":
    main()
