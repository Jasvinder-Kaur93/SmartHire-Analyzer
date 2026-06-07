import re
import spacy
from pdfminer.high_level import extract_text
from docx import Document

nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(file):
    return extract_text(file)


def extract_text_from_docx(file):

    doc = Document(file)

    return "\n".join(
        [p.text for p in doc.paragraphs]
    )


def extract_contact_info(text):

    email = re.findall(
        r'\S+@\S+',
        text
    )

    phone = re.findall(
        r'\+?\d[\d -]{8,}\d',
        text
    )

    name = None

    doc = nlp(text)

    for ent in doc.ents:

        if ent.label_ == "PERSON":
            name = ent.text
            break

    return {

        "name": name if name else "Not Found",

        "email": (
            email[0]
            if email else "Not Found"
        ),

        "phone": (
            phone[0]
            if phone else "Not Found"
        )
    }
def extract_experience(text):
    pattern = r'(\d+)\+?\s+years'

    matches = re.findall(
        pattern,
        text.lower()
    )
    if matches:
        return max(matches)
    return "0"