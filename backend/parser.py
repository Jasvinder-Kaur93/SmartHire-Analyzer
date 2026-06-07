import re
import spacy
from pdfminer.high_level import extract_text
from docx import Document

# Cloud-safe NLP (NO MODEL)
nlp = spacy.blank("en")


def extract_text_from_pdf(file):
    return extract_text(file)


def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])


def extract_contact_info(text):

    email = re.findall(r'\S+@\S+', text)
    phone = re.findall(r'\+?\d[\d -]{8,}\d', text)

    # Simple name guess
    name = None
    lines = text.split("\n")

    for line in lines[:10]:
        words = line.strip().split()
        if 1 < len(words) <= 4:
            if all(w.isalpha() for w in words):
                name = line.strip()
                break

    return {
        "name": name if name else "Not Found",
        "email": email[0] if email else "Not Found",
        "phone": phone[0] if phone else "Not Found"
    }


def extract_experience(text):
    pattern = r'(\d+)\+?\s+years'
    matches = re.findall(pattern, text.lower())

    return max(matches) if matches else "0"
