from io import BytesIO
from docx import Document
from formatters.common import sanitize_text, safe_filename
from formatters.docx_formatter import format_docx
from formatters.pdf_formatter import format_pdf
from formatters.text_formatter import format_txt

def test_sanitize():
    assert sanitize_text("Hello—world“!") == 'Hello-world"!'
    assert safe_filename("NDA / Test") == "NDA_Test"

def test_txt(): assert format_txt("Hello") == b"Hello"

def test_docx():
    data = format_docx("1. Confidentiality\nThe parties agree.", "NDA", terms=["Keep information confidential"])
    doc = Document(BytesIO(data)); text = "\n".join(p.text for p in doc.paragraphs)
    assert "NDA" in text and "Confidentiality" in text

def test_pdf(): assert format_pdf("1. Confidentiality\nThe parties agree.", "NDA").startswith(b"%PDF")
