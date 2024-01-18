import PyPDF2

def extractPDF(file):
  pdf_reader = PyPDF2.PdfReader(file)

  textpdf = ''

  for i in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[i]
    textpdf += page.extract_text()

  return textpdf

def extractPDFPerPage(filepath):
  pdfReader = PyPDF2.PdfReader(filepath)

  textPDF = [page.extract_text() for page in pdfReader.pages]

  return textPDF