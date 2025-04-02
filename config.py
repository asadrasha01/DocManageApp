import os

# Directory settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "data", "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")
LOG_FILE = os.path.join(BASE_DIR, "logs", "app.log")
FONT_PATH = os.path.join(BASE_DIR, "fonts", "DejaVuSans.ttf")  # or adjust if needed

# Text processing settings
DEFAULT_SUMMARY_SENTENCES = 3
SUPPORTED_FILE_TYPES = [".txt", ".docx", ".pdf", ".png", ".jpg", ".jpeg"]

# Logging level
LOG_LEVEL = "INFO"
