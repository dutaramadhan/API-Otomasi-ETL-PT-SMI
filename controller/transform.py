import re
from controller import extract
from langchain.text_splitter import NLTKTextSplitter
import nltk
nltk.download('punkt')

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

def recursive_split(patterns, texts, header):
  results = []
  headers = []
  pattern = patterns[0]
  for i in range(len(texts)):
    cur_results, cur_header = splitTextBy(pattern, texts[i], header[i])
    next_patterns = patterns[1:]

    if not next_patterns:
      results.extend(cur_results)
      headers.extend(cur_header)
    else:
      next_results, next_header = recursive_split(next_patterns, cur_results, cur_header)
      results.extend(next_results)
      headers.extend(next_header)

  return results, headers

def textSplit(textpdf, split_patterns, resplit_patterns):
  chunks = []

  results = [textpdf]
  header = ['']
  
  results, header = recursive_split(split_patterns, results, header)
  print(results)
  # split by chunk size
  text_splitter = NLTKTextSplitter(chunk_size=2000)
  for k in range(len(results)):
    texts = text_splitter.split_text(results[k])
    for text in texts:
      chunks.append(header[k] + '\n' + text)

  for pattern in resplit_patterns:
    for i in range(len(chunks)):
      matches = re.findall(pattern, chunks[i])
      if matches:
        split_last = re.split(pattern, chunks[i])
        chunks[i] = split_last[0]
        chunks.insert(i + 1, split_last[1])

  return [item for item in chunks if item]

def transform_pasal(textpdf, filename, unnecessary_patterns, title_patterns, split_patterns, resplit_patterns):
  # Delete unnecessary pattern
  result = cleanText(unnecessary_patterns, textpdf)

  # Split Text
  chunks = textSplit(result, split_patterns, resplit_patterns)

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