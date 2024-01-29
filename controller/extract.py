import PyPDF2
import fitz

def extract_pdf(filepath):
  """
  with open(filepath, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)

    textpdf = ''

    for i in range(len(pdf_reader.pages)):
      page = pdf_reader.pages[i]
      textpdf += page.extract_text()
  """
  doc = fitz.open(filepath)

  for page_num in range(doc.page_count):
    page = doc[page_num]
    textpdf += page.get_text()
    
  return textpdf

def extract_pdf_per_page(filepath):
  with open(filepath, 'rb') as file:
    pdfReader = PyPDF2.PdfReader(filepath)

    textPDF = [page.extract_text() for page in pdfReader.pages]

  return textPDF