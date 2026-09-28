from io import BytesIO
from pathlib import Path
from fpdf import FPDF
from .common import DEFAULT_LOGO, sanitize_text

class LegalEasePDF(FPDF):
    def __init__(self, company_name):
        super().__init__(); self.company_name = company_name; self.set_auto_page_break(auto=True, margin=18)
    def header(self):
        self.set_font("Times", "B", 9); self.cell(0, 6, self.company_name, align="C"); self.ln(7)
    def footer(self):
        self.set_y(-14); self.set_font("Times", "I", 8)
        self.cell(0, 8, f"{self.company_name} - AI-generated draft | Page {self.page_no()}", align="C")

def format_pdf(text, doc_type, terms=None, logo_path=None, company_name="LegalEase"):
    pdf = LegalEasePDF(company_name); pdf.add_page()
    chosen_logo = Path(logo_path) if logo_path else DEFAULT_LOGO
    if chosen_logo.exists() and chosen_logo.suffix.lower() in {".png", ".jpg", ".jpeg"}:
        pdf.image(str(chosen_logo), x=pdf.w / 2 - 12, y=18, w=24); pdf.ln(27)
    pdf.set_font("Times", "B", 15); pdf.multi_cell(0, 9, sanitize_text(doc_type).upper(), align="C"); pdf.ln(4)
    pdf.set_font("Times", "", 11)
    for raw in sanitize_text(text).splitlines():
        line = raw.strip()
        if not line: pdf.ln(3); continue
        if line.startswith("#"):
            pdf.ln(2); pdf.set_font("Times", "B", 12); pdf.multi_cell(0, 7, line.lstrip("# ").strip()); pdf.set_font("Times", "", 11)
        elif line.startswith(("-", "*")):
            pdf.multi_cell(0, 6, "- " + line[1:].strip())
        else:
            pdf.multi_cell(0, 6, line)
        pdf.ln(1)
    if terms:
        pdf.ln(3); pdf.set_font("Times", "B", 12); pdf.cell(0, 7, "Key Terms"); pdf.ln(8); pdf.set_font("Times", "", 10)
        for idx, term in enumerate(terms, 1): pdf.multi_cell(0, 6, f"{idx}. {sanitize_text(term)}")
    return bytes(pdf.output())
