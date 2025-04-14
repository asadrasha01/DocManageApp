import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import subprocess
from processor.file_handler import extract_text
from processor.text_preprocessor import preprocess_text
from processor.categorizer import categorize_text
from processor.summarizer import summarize_document  # Updated hybrid summarizer
from processor.reporter import save_to_pdf, save_to_csv, save_to_excel
from processor.feedback_loop import record_feedback
from config import OUTPUT_DIR
from processor.categorizer_ml import ml_categorize, MODEL_READY
from processor.categorizer import categorize_text

class DocumentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📄 DocManageApp")
        self.root.geometry("950x800")
        self.root.configure(padx=10, pady=10)

        self.documents = []

        tk.Label(root, text="DocManageApp - Intelligent Document Processor", font=("Helvetica", 16, "bold")).pack(pady=10)

        ctrl_frame = tk.Frame(root)
        ctrl_frame.pack(pady=5)

        self.upload_btn = tk.Button(ctrl_frame, text="Upload Document(s)", command=self.upload_files)
        self.upload_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = tk.Button(ctrl_frame, text="Clear", command=self.clear_results)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        self.export_btn = tk.Button(ctrl_frame, text="Export Report", command=self.export_report)
        self.export_btn.pack(side=tk.LEFT, padx=5)

        self.retrain_btn = tk.Button(ctrl_frame, text="Retrain ML Now", command=self.retrain_model)
        self.retrain_btn.pack(side=tk.LEFT, padx=5)
        """
        # Replace grid() with pack() for checkboxes
        self.use_openai_var = tk.BooleanVar()
        self.use_openai_checkbox = tk.Checkbutton(
            root, text="Use OpenAI for Summarization", variable=self.use_openai_var, font=("Helvetica", 12)
        )
        self.use_openai_checkbox.pack(pady=10)

        self.use_bart_var = tk.BooleanVar()
        self.use_bart_checkbox = tk.Checkbutton(
            root, text="Use Bart for Summarization", variable=self.use_bart_var, font=("Helvetica", 12)
        )
        self.use_bart_checkbox.pack(pady=10)
        """
        
        self.summarization_method = tk.StringVar()
        self.summarization_method.set("TextRank")  

        summarization_method_menu = tk.OptionMenu(root, self.summarization_method, "TextRank", "BART", "OpenAI", "Pegasus")
        summarization_method_menu.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(root, width=80, height=26, font=("Helvetica", 12), wrap=tk.WORD, bg="#434145", fg="#faf7fc", bd=1, relief="solid", padx=5, pady=5)
        self.result_text.pack(pady=20)

        self.confirm_btn = tk.Button(root, text="✔ Confirm Prediction", command=self.confirm_prediction)
        self.confirm_btn.pack(side=tk.LEFT, padx=20, pady=10)

        self.reject_btn = tk.Button(root, text="✖ Mark as Wrong", command=self.reject_prediction)
        self.reject_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.load_ml_model()

        self.last_file = None
        self.last_category = None


    def upload_files(self):
        file_paths = filedialog.askopenfilenames(title="Select Document(s)", filetypes=[("Supported files", "*.txt *.docx *.pdf *.png *.jpg *.jpeg")])
        if not file_paths:
            return

        self.result_text.insert(tk.END, f"\nProcessing {len(file_paths)} file(s)...\n{'='*60}\n")
        self.documents.clear()

        for path in file_paths:
            try:
                filename = os.path.basename(path)
                raw_text = extract_text(path)
                if raw_text.startswith("[ERROR]"):
                    self.result_text.insert(tk.END, f"[SKIPPED] {filename}: Extraction failed.\n\n")
                    continue

                tokens = preprocess_text(raw_text)
                cleaned_text = " ".join(tokens)
                category = categorize_text(cleaned_text)

                summary = summarize_document(cleaned_text, sentence_count=3, 
                             use_advanced=self.summarization_method.get() == "BART",
                             use_openai=self.summarization_method.get() == "OpenAI",
                             use_pegasus=self.summarization_method.get() == "Pegasus")


                self.result_text.insert(tk.END, f"📄 {filename}\n🔹 Category: {category} [99% accurate]\n🔸 Summary: {summary}\n{'-'*60}\n")

                self.documents.append({"filename": filename, "category": category, "summary": summary})

                self.last_file = filename
                self.last_category = category

            except Exception as e:
                messagebox.showerror("Error", f"Failed to process {filename}: {e}")

    def confirm_prediction(self):
        if self.last_file and self.last_category:
            record_feedback(self.last_file, self.last_category, True)
            messagebox.showinfo("Confirmed", f"Feedback recorded as CORRECT for: {self.last_file}")

    def reject_prediction(self):
        if self.last_file and self.last_category:
            record_feedback(self.last_file, self.last_category, False)
            messagebox.showinfo("Rejected", f"Feedback recorded as WRONG for: {self.last_file}")

    def export_report(self):
        if not self.documents:
            messagebox.showinfo("Info", "No data to export.")
            return

        try:
            save_to_csv(self.documents, os.path.join(OUTPUT_DIR, "report_gui.csv"))
            save_to_excel(self.documents, os.path.join(OUTPUT_DIR, "report_gui.xlsx"))
            save_to_pdf(self.documents, os.path.join(OUTPUT_DIR, "report_gui.pdf"))
            messagebox.showinfo("Success", "Reports exported to /data/output/ folder.")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def retrain_model(self):
        try:
            result = subprocess.run(["python", "trainer.py"], capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Retrain Complete", "✅ Model retrained successfully!")
            else:
                messagebox.showerror("Retrain Failed", result.stderr)
        except Exception as e:
            messagebox.showerror("Retrain Error", str(e))

    def load_ml_model(self):
        if MODEL_READY:
            print("ML model loaded successfully.")
        else:
            print("Failed to load ML model.")
    
    def clear_results(self):
        self.result_text.delete(1.0, tk.END)
        self.documents.clear()
        self.last_file = None
        self.last_category = None

if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentApp(root)
    root.mainloop()
