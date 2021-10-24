import pdftotext
import re

# convert PDF
# split into pages and lines
with open('6162_EMRAP_2020_02_February_Written_Summary.pdf', 'rb') as f:
  doc = [page.split('\n') for page in pdftotext.PDF(f)]


