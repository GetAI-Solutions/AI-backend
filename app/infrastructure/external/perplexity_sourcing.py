import requests

def get_details_from_perplexity(product_name, auth_token, url = "https://api.perplexity.ai/chat/completions"):
    payload = {
    "model": "llama-3.1-sonar-small-128k-online",
    "messages": [
        {
            "content": "string",
            "role": "system"
        },
        {
            "content":f" Please give me details about the following prouct - {product_name}",
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
        "authorization": f"Bearer {auth_token}"

    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()["choices"][0]["message"]["content"]