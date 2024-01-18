import os
import json
from dotenv import load_dotenv
import requests

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

    return response