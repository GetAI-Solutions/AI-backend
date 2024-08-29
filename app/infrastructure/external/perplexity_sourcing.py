import requests
from config import Perplexity_KEY

def get_details_from_perplexity(product_name, url = "https://api.perplexity.ai/chat/completions"):
    payload = {
    "model": "llama-3.1-sonar-small-128k-online",
    "messages": [
        {
            "content": "string",
            "role": "system"
        },
        {
            "content":f" Please give me extensive details about the following prouct - {product_name}. Ensure to include as much information as possible",
            "role": "user"
        }
    ],
    "max_tokens": 0,
    "temperature": 0.2,
    "top_p": 0.9,
    "return_citations": False,
    "return_images": False,
    "return_related_questions": False,
    "top_k": 0,
    "stream": False,
    "presence_penalty": 0,
    "frequency_penalty": 1
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {Perplexity_KEY}"

    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()["choices"][0]["message"]["content"]