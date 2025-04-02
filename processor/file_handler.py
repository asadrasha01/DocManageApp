import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF is used for working with PDF files
import docx  # python-docx for reading DOCX files

# Function to extract text from a TXT file
def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()  # Read and return the entire content of the file
    except Exception as e:
        return f"[ERROR] Failed to read TXT file: {e}"  # Return error message if reading fails

# Function to extract text from a DOCX file
def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)  # Load the DOCX document
        return "\n".join([para.text for para in doc.paragraphs])  # Join all paragraph texts with newline
    except Exception as e:
        return f"[ERROR] Failed to read DOCX file: {e}"  # Return error message if reading fails

# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)  # Open the PDF file
        text = ""
        for page in doc:
            text += page.get_text()  # Extract text from each page and append to result
        return text
    except Exception as e:
        return f"[ERROR] Failed to read PDF file: {e}"  # Return error message if reading fails

# Function to extract text from an image using OCR
def extract_text_from_image(file_path):
    try:
        image = Image.open(file_path)  # Open the image file
        return pytesseract.image_to_string(image)  # Use OCR to extract text
    except Exception as e:
        return f"[ERROR] Failed to read image file: {e}"  # Return error message if reading fails

# General function to extract text based on file extension
def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()  # Extract the file extension in lowercase
    if ext == ".txt":
        return extract_text_from_txt(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(file_path)
    else:
        return "[ERROR] Unsupported file type."  # Return an error if file type is not supported

# Test block for standalone usage
if __name__ == "__main__":
    sample_file = "../data/input/sample.pdf"  # Specify a sample file path for testing
    print(extract_text(sample_file))  # Print extracted text from the sample file