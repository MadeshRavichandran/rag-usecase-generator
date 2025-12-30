import os
import pdfplumber
import yaml
from docx import Document

def load_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in [".txt", ".md"]:
        return open(path, "r", encoding="utf-8").read()
    
    if ext == ".pdf":
        try:
            text = ""
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"[WARN] Skipping invalid PDF: {path} ({e})")
            return ""
    
    if ext in [".yaml", ".yml"]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return yaml.dump(data)
        except Exception as e:
            print(f"[WARN] Invalid YAML, loading as raw text: {path} ({e})")
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

    
    if ext == ".docx":
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)

    raise ValueError(f"Unsupported file type: {ext}")
