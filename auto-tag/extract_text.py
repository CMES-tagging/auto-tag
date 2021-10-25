# convert PDF; split into pages and lines
import pdftotext

def pdf_to_text(filename):
    with open(filename, 'rb') as f:
        doc = [page.split('\n') for page in pdftotext.PDF(f)]
    return doc

