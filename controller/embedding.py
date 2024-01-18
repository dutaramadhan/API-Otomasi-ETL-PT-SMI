import os
import json
from dotenv import load_dotenv
import requests
import time
import model
from controller import transform
import threading

load_dotenv()

def get_embedding(text):
    url = "https://api.openai.com/v1/embeddings"

    payload = json.dumps({
        "input": text,
        "model": "text-embedding-ada-002",
        "encoding_format": "float"
    })
    headers = {
        'Authorization': 'Bearer ' + os.getenv('API_KEY'),
        'Content-Type': 'application/json',
        'Cookie': '__cf_bm=Ghr17uXmAZAP3sAagI5nlm2Ex4fSgiGKZGkREvPnsOw-1704772804-1-AUlILWecFQtgsKkszWgeW2iUzF6M/ai9qRJVSxnA0/NP7bCdqWX4CmsGjo4F6UP7n382NwuTgTNV/RWe2GfcqEM=; _cfuvid=1fYoJQCnpqqs.xdVCMebdMShJREPBmizEhyzPI.C9cE-1704772804555-0-604800000'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()

def embedding_content(content, source_title):
    text = source_title + '\n' + content
    response_embedding = get_embedding(text)
    embedding_vector = response_embedding['data'][0]['embedding']
    token = response_embedding['usage']['total_tokens']
    return embedding_vector, token

def embedding_header(content, source_name, source_title):
    header = transform.getHeader(source_name, source_title, content)
    if header == None:
        header_embedding_vector = None
    else:
        header_embedding = get_embedding(header)
        header_embedding_vector = header_embedding['data'][0]['embedding']
    return header_embedding_vector

def create_embeddings(source_id, header=False):
    while True:
        data = model.selectOne(source_id)
        if not data:
            print("completed")
            break
        [content, source_title, source_name, id] = data

        embedding_vector, token = embedding_content(content, source_title)

        header_embedding_vector = None
        if header:
            header_embedding_vector = embedding_header(content, source_name, source_title)

        model.storeEmbedding(int(id), embedding_vector, int(token), header_embedding_vector)

        print(id, token)
        time.sleep(60/500)
    return True

def threaded_create_embeddings(source_id, header=False):
    thread = threading.Thread(target=create_embeddings, args=(source_id, header))
    thread.start()
