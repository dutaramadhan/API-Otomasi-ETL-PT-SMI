import re
from controller import extract
from langchain.text_splitter import NLTKTextSplitter
import nltk

def splitTextBy(pattern, text, context=""):
  result = re.split(pattern, text)
  chunks = result[::2]
  context = [context] + [context + ctx.replace('\n', ' ').strip() + '. ' for ctx in result[1::2]]
  return chunks, context

def cleanText(unnecessary_patterns, text):
  result = text
  for pattern in unnecessary_patterns:
    result = re.sub(pattern, '', result)
  return result

def findTitle(title_patterns, chunk):
  title = ''
  for pattern in title_patterns:
    matches = re.findall(pattern, chunk)
    if matches:
        title = matches[0].strip()
        title = re.sub('\n', ' ', title)
        break
  return title

def textSplit(textpdf):
  chunks = []

  # Split Penjelasan
  result, context = splitTextBy(r'\s*(PENJELASAN)\s*\n', textpdf)

  # Split Bab
  for i in range(len(result)):
    bab_pattern = r'(\n\s*BAB [IXVLCM]+\s*\n.*)'
    bab_text, bab = splitTextBy(bab_pattern, result[i], context[i])

    # Split Pasal
    for j in range(len(bab)):
      pasal_pattern = r'(\n\s*Pasal \d+\s*\n)'
      pasal_text, pasal = splitTextBy(pasal_pattern, bab_text[j], bab[j])

      # store
      for k in range(len(pasal)):
        text_splitter = NLTKTextSplitter(chunk_size=2000)
        texts = text_splitter.split_text(pasal_text[k])
        for text in texts:
          chunks.append(pasal[k] + '\n' + text)

  split_patterns = [
        (r'(Disahkan [\s\S]+)', 1),
        (r'(Ditetapkan [\s\S]+)', 1)
    ]

  for pattern, insert_index in split_patterns:
    for i in range(len(chunks)):
      matches = re.findall(pattern, chunks[i])
      if matches:
        split_last = re.split(pattern, chunks[i])
        chunks[i] = split_last[0]
        chunks.insert(i + insert_index, split_last[1])

  return [item for item in chunks if item]

def transform_pasal(textpdf, filename, unnecessary_patterns, title_patterns):
  # Delete unnecessary pattern
  result = cleanText(unnecessary_patterns, textpdf)

  # Split Text
  chunks = textSplit(result)

  # Find Title
  title = findTitle(title_patterns, chunks[0])
  if title == '':
    title = re.sub('.pdf|.PDF', '', filename)

  return title, chunks

def transform_non_pasal(textpdf, filename, unnecessary_patterns, title_patterns):
  # Extract 
  chunks = extract.extractPDFPerPage(textpdf)

  # Delete unnecessary pattern
  for i in range(len(chunks)):
    chunks[i] = cleanText(unnecessary_patterns, chunks[i])

  # Find Title
  title = findTitle(title_patterns, chunks[0])
  if title == '':
    title = re.sub('.pdf|.PDF', '', filename)

  return title, [item for item in chunks if item]

def getHeader(source_name, source_title, content):
  try :
    [penjelasan, pasal] = re.split(r'(Pasal \d+)', content)[0:2]
    name = re.split('\.', source_name)[0]
    title = re.split(r'TENTANG', source_title)[0]

    header = name + ' ' + title + ' '

    if re.findall(r'penjelasan', penjelasan, re.IGNORECASE):
      header += penjelasan + ' '

    header += pasal
    return header

  except Exception as e:
    return None