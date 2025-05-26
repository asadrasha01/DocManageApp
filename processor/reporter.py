import os
import pandas as pd
from fpdf import FPDF
from config import FONT_PATH, OUTPUT_DIR

def sanitize_text(text):
    if not isinstance(text, str):
        return ""
    return text.encode("latin1", errors="replace").decode("latin1")

def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_individual_reports(item):
    filename = item.get("filename", "")
    category = item.get("category", "Uncategorized")
    summary = item.get("summary", "")
    
    if not filename:
        return

    base_name = os.path.splitext(os.path.basename(filename))[0]
    folder_path = os.path.join(OUTPUT_DIR, base_name)
    ensure_folder(folder_path)

    data = {
        "filename": [filename],
        "category": [category],
        "summary": [summary]
    }

    # Save CSV
    pd.DataFrame(data).to_csv(os.path.join(folder_path, "report.csv"), index=False)
    # Save Excel
    pd.DataFrame(data).to_excel(os.path.join(folder_path, "report.xlsx"), index=False)

    # Save PDF
    pdf = FPDF()
    pdf.add_page()
    try:
        pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
        pdf.set_font("DejaVu", size=12)
    except:
        pdf.set_font("Arial", size=12)

    line = f"Filename: {sanitize_text(filename)}\nCategory: {sanitize_text(category)}\nSummary: {sanitize_text(summary)}"
    pdf.multi_cell(0, 10, line + "\n------------------------\n")
    pdf.output(os.path.join(folder_path, "report.pdf"))

def generate_all_reports(data_list):
    for item in data_list:
        save_individual_reports(item)

# Example usage
if __name__ == "__main__":
    sample_data = [
        {"filename": "doc1.pdf", "category": "Finance", "summary": "Bank account and payment details."},
        {"filename": "doc2.docx", "category": "Education", "summary": "University courses and schedules."}
    ]
    generate_all_reports(sample_data)
