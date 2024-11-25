from PyPDF2 import PdfReader

def read_pdf(file_path):
    """Read PDF file and extract text."""
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()