import fitz

def extract_pdf(filepath):
  doc = fitz.open(filepath)
  textpdf = ''
  for page_num in range(doc.page_count):
    page = doc[page_num]
    textpdf += page.get_text()

  return textpdf

def extract_pdf_per_page(filepath):
  doc = fitz.open(filepath)

  textPDF = [doc[page_num].extract_text() for page_num in range(doc.page_count)]

  return textPDF