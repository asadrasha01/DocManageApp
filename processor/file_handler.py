import os
import pytesseract
from PIL import Image
import fitz 
import docx  


def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()  
    except Exception as e:
        return f"[ERROR] Failed to read TXT file: {e}"

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)  
        return "\n".join([para.text for para in doc.paragraphs])  
    except Exception as e:
        return f"[ERROR] Failed to read DOCX file: {e}"  


def extract_text_from_pdf(file_path):
    try:
        doc = fitz.open(file_path) 
        text = ""
        for page in doc:
            text += page.get_text()  
        return text
    except Exception as e:
        return f"[ERROR] Failed to read PDF file: {e}"  


def extract_text_from_image(file_path):
    try:
        image = Image.open(file_path)  
        return pytesseract.image_to_string(image)  
    except Exception as e:
        return f"[ERROR] Failed to read image file: {e}"  


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower() 
    if ext == ".txt":
        return extract_text_from_txt(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(file_path)
    else:
        return "[ERROR] Unsupported file type."  


if __name__ == "__main__":
    sample_file = "../data/input/sample.pdf"  
    print(extract_text(sample_file)) 