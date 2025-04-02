# DocManageApp 📄

## Overview

DocManageApp is an intelligent document processing application designed to automate the classification and summarization of documents. The app utilizes **Machine Learning (ML)** and **Rule-based models** to categorize various types of documents such as CVs, invoices, contracts, and more.

### Features 🚀

- **Document Categorization**: Categorize documents into various predefined categories (Finance, HR, Medical, etc.) using ML and rule-based methods.
- **Document Summarization**: Generate concise summaries for documents, configurable by sentence length.
- **User Feedback Integration**: Collect user feedback for accurate predictions and automatic retraining of the model.
- **Export Reports**: Generate reports in **CSV**, **Excel**, and **PDF** formats.
- **Retrain Model**: Retrain the ML model with new feedback through a simple click in the GUI.

## Requirements 🛠

- Python 3.8+
- `nltk` (for text preprocessing)
- `transformers` (for LLM fallback)
- `scikit-learn` (for ML classification)
- `fpdf` (for PDF report generation)
- `pandas` (for CSV and Excel reports)

## Installation 🔧

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/DocManageApp.git
   cd DocManageApp
   ```

## Step 2: Set up the virtual environment

    python -m venv venv
    source venv/bin/activate  # on Windows, use `venv\\Scripts\\activate`

## Step 3: Install the dependencies

    pip install -r requirements.txt

## Step 4: Download any necessary nltk data

    python -m nltk.downloader punkt stopwords

# Running the App ▶️

## CLI

To run the application from the command line:

    python main.py

## GUI 🖥️

For the graphical user interface, simply run:

    python gui.py

Retraining the Model 🔄
To retrain the machine learning model with user feedback:

Upload documents and validate predictions in the GUI.

Click Retrain ML Now to retrain the model.

## Testing 🧪

To run unit tests:

    python -m unittest discover -s tests

## License 📜

This project is licensed under the MIT License.

## Acknowledgements 🙏

Inspired by various NLP tools and libraries.

Thanks to the contributors of scikit-learn, transformers, and other used libraries.

Contact Information 📬
Feel free to reach out for any contributions, suggestions, or feedback.
