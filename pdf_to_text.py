# pdf_to_text.py
import pdfplumber

def extract_text(pdf_path):
    """
    Extracts text from a PDF file using pdfplumber.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from all pages of the PDF.
    """
    all_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text + "\n"
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")

    return all_text



