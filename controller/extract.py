import PyPDF2

def extract_pdf(filepath):
  with open(filepath, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)

    textpdf = ''

    for i in range(len(pdf_reader.pages)):
      page = pdf_reader.pages[i]
      textpdf += page.extract_text()

  return textpdf

def extract_pdf_per_page(filepath):
  with open(filepath, 'rb') as file:
    pdfReader = PyPDF2.PdfReader(filepath)

    textPDF = [page.extract_text() for page in pdfReader.pages]

  return textPDF