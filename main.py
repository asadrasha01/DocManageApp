import os
import argparse
import logging
from processor.file_handler import extract_text
from processor.text_preprocessor import preprocess_text
from processor.categorizer import categorize_text
from processor.summarizer import summarize_text
from processor.reporter import save_to_csv, save_to_excel, save_to_pdf
from processor.feedback_loop import ask_user_feedback, record_feedback
from config import (
    INPUT_DIR as DEFAULT_INPUT,
    OUTPUT_DIR as DEFAULT_OUTPUT,
    LOG_FILE,
    LOG_LEVEL,
    DEFAULT_SUMMARY_SENTENCES,
    SUPPORTED_FILE_TYPES
)

# --------------------------
# Setup argument parser
# --------------------------
parser = argparse.ArgumentParser(description="Intelligent Document Processor")
parser.add_argument("--input", type=str, default=DEFAULT_INPUT, help="Input folder path")
parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT, help="Output folder path")
parser.add_argument("--summary-lines", type=int, default=DEFAULT_SUMMARY_SENTENCES, help="Number of sentences in summary")
args = parser.parse_args()

# --------------------------
# Setup logging
# --------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --------------------------
# Ensure output directory exists
# --------------------------
os.makedirs(args.output, exist_ok=True)

# --------------------------
# Process files
# --------------------------
processed_docs = []

for filename in os.listdir(args.input):
    file_path = os.path.join(args.input, filename)

    # Skip directories, hidden files, and unsupported types
    if not os.path.isfile(file_path) or filename.startswith("."):
        continue

    ext = os.path.splitext(filename)[1].lower()
    if ext not in SUPPORTED_FILE_TYPES:
        print(f"[SKIPPED] {filename}: Unsupported file type")
        continue

    print(f"Processing file: {filename}")
    logging.info(f"Started processing file: {filename}")

    raw_text = extract_text(file_path)

    if raw_text.startswith("[ERROR]"):
        print(raw_text)
        logging.error(f"Extraction failed for {filename}: {raw_text}")
        continue

    tokens = preprocess_text(raw_text)
    cleaned_text = " ".join(tokens)

    category = categorize_text(cleaned_text)
    summary = summarize_text(cleaned_text, sentence_count=args.summary_lines)

    # Ask for user feedback and record it
    confirmed = ask_user_feedback(filename, category)
    record_feedback(filename, category, confirmed)
    logging.info(f"Feedback recorded for {filename}: {'confirmed' if confirmed else 'not confirmed'}")

    processed_docs.append({
        "filename": filename,
        "category": category,
        "summary": summary
    })

    logging.info(f"File categorized as: {category}")
    logging.info(f"Summary generated for: {filename}")

# --------------------------
# Save results
# --------------------------
save_to_csv(processed_docs, os.path.join(args.output, "report.csv"))
save_to_excel(processed_docs, os.path.join(args.output, "report.xlsx"))
save_to_pdf(processed_docs, os.path.join(args.output, "report.pdf"))

print("\nDocument processing complete. Reports saved to output folder.")
logging.info("All documents processed. Reports saved.")
